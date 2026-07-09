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


// exercise the communicator factories: {split}, {duplicate}, and {compare}
int
main()
{
    // bring mpi up
    pyre::mpi::initialize();

    // push down a scope so our handles die before mpi does
    {
        // the communicator that holds the whole job
        auto world = pyre::mpi::world();
        // its size
        auto size = world.size();
        // and my rank in it
        auto rank = world.rank();

        // split the world by the parity of the rank, preserving the world order within each
        // half by using the rank itself as the key
        auto half = world.split(rank % 2, rank);
        // the even ranks are the ones mpi rounds up
        auto expected = (rank % 2 == 0) ? (size + 1) / 2 : size / 2;
        // so each half holds the processes of its own parity
        assert(half.size() == expected);
        // and my rank within my half counts the processes of my parity that precede me
        assert(half.rank() == rank / 2);

        // a process that offers {undefined} as its color asks to be left out entirely
        auto nobody = world.split(pyre::mpi::undefined, rank);
        // and gets the null communicator back
        assert(nobody.isNull());

        // duplicating the world preserves its membership
        auto twin = world.duplicate();
        // so the sizes agree
        assert(twin.size() == size);
        // and so do the ranks
        assert(twin.rank() == rank);
        // but the context is fresh, which is exactly what {congruent} means
        assert(world.compare(twin) == pyre::mpi::Comparison::congruent);

        // a communicator is identical to itself
        assert(world.compare(world) == pyre::mpi::Comparison::identical);

        // when the job holds more than one process, the halves are strictly smaller than the
        // whole, so they cannot even be congruent to it
        if (size > 1) {
            assert(world.compare(half) == pyre::mpi::Comparison::unequal);
        }

        // the groups behave the same way: my half's group is a subset of the world's
        auto whole = world.group();
        // so comparing them reports nothing in common in the ordering sense
        assert(whole.compare(whole) == pyre::mpi::Comparison::identical);

        // translating my world rank into my half's group tells me where i landed
        auto mine = half.group();
        // ask for the answer
        auto translated = whole.translateRanks({ rank }, mine);
        // which must be the rank i already know i have
        assert(translated.size() == 1);
        // and it must agree with what the communicator says
        assert(translated[0] == half.rank());
    }

    // take mpi down
    pyre::mpi::finalize();

    // all done
    return 0;
}


// end of file
