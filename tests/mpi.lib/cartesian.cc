// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// for the build system
#include <portinfo>
// other packages
#include <cassert>
// grab the mpi objects
#include <pyre/mpi.h>


// exercise the cartesian topology: laying the processes out on a grid, walking it, and
// carving sub-grids out of it
int
main()
{
    // bring mpi up
    pyre::mpi::initialize();

    // push down a scope so our handles die before mpi does
    {
        // the communicator that holds the whole job
        auto world = pyre::mpi::world();
        // this test is launched with exactly eight processes, so it can lay them out on a
        // grid whose shape it knows ahead of time
        assert(world.size() == 8);

        // arrange them on a two by four grid, wrapping the second axis only
        pyre::mpi::shape_t shape { 2, 4 };
        // so that walking along it comes back around
        pyre::mpi::shape_t periods { 0, 1 };
        // let mpi renumber the processes if it can do better
        auto grid = world.cartesian(shape, periods, 1);

        // the grid has two axes
        assert(grid.dimensions() == 2);
        // whose extents are the ones we asked for
        assert(grid.shape() == shape);
        // and whose periodicity is what we asked for
        assert(grid.periods() == periods);

        // my rank on the grid, which need not be my rank in the world
        auto rank = grid.rank();
        // where i sit
        auto here = grid.coordinates(rank);
        // one coordinate per axis
        assert(here.size() == 2);
        // and both are within the grid
        assert(here[0] >= 0 && here[0] < shape[0]);
        assert(here[1] >= 0 && here[1] < shape[1]);

        // asking for the rank at my own coordinates must bring me back to myself
        assert(grid.rank(here) == rank);

        // the second axis wraps, so stepping along it always lands on a real process
        auto [before, after] = grid.shift(1, 1);
        // in both directions
        assert(before != pyre::mpi::procNull);
        assert(after != pyre::mpi::procNull);
        // and my successor's predecessor is me
        assert(grid.coordinates(after)[1] == (here[1] + 1) % shape[1]);

        // the first axis does not wrap, so exactly one of the two processes at its ends falls
        // off the grid
        auto [above, below] = grid.shift(0, 1);
        // the process on the low edge has nobody above it
        if (here[0] == 0) {
            assert(above == pyre::mpi::procNull);
        }
        // and the one on the high edge has nobody below it
        if (here[0] == shape[0] - 1) {
            assert(below == pyre::mpi::procNull);
        }

        // carve out the sub-grid that keeps only the second axis, so each row becomes its own
        // cartesian communicator
        auto row = grid.sub({ 0, 1 });
        // which has one axis
        assert(row.dimensions() == 1);
        // holding the four processes of my row
        assert(row.size() == shape[1]);
        // and my position along it is my second coordinate
        assert(row.coordinates(row.rank())[0] == here[1]);

        // a shape that names no axes is not a grid
        bool refused = false;
        // so ask for one
        try {
            // and watch it fail
            world.cartesian({}, {}, 0);
        }
        // the package refuses with a shape error, not with an mpi status of zero, which is the
        // code mpi reserves for success
        catch (const pyre::mpi::ShapeError &) {
            refused = true;
        }
        // check that it did
        assert(refused);

        // a shape whose axes do not all say whether they wrap is not a grid either
        refused = false;
        // so ask for one
        try {
            // and watch it fail
            world.cartesian({ 2, 4 }, { 0 }, 0);
        }
        // again, a shape error
        catch (const pyre::mpi::ShapeError &) {
            refused = true;
        }
        // check that it did
        assert(refused);
    }

    // take mpi down
    pyre::mpi::finalize();

    // all done
    return 0;
}


// end of file
