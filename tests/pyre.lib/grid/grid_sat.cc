// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// a non-trivial example: a sum area table; the calculations are done with raw indices
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("grid_sat");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.sat");

    // we'll work with a 3d conventionally packed grid
    using pack_t = pyre::grid::canonical_t<2>;
    // of doubles on the heap
    using storage_t = pyre::memory::heap_t<double>;
    // putting it all together
    using grid_t = pyre::grid::grid_t<pack_t, storage_t>;

    // pick the shape
    pack_t::shape_type shape { 1024, 1024 };
    // packing: 1024x1024
    pack_t packing { shape };
    // instantiate the grid
    grid_t grid { packing, packing.cells() };
    // pick a value
    double value = 1;
    // fill it
    for (const auto & idx : grid.layout()) {
        // with our chosen value
        grid[idx] = value;
    }

    // make the sum area table
    grid_t sat { packing, packing.cells() };

    // fill the top corner
    sat[{0,0}] = grid[{0,0}];
    // fill the top row
    for (auto col=1; col < shape[1]; ++col) {
        // just skip the terms that would cause out of bounds accesses
        sat[{0,col}] = grid[{0,col}] + sat[{0,col-1}];
    }
    // fill the left column
    for (auto row=1; row < shape[0]; ++row) {
        // just skip the terms that would cause out of bounds accesses
        sat[{row,0}] = grid[{row,0}] + sat[{row-1,0}];
    }
    // fill the rest of the table
    for (auto row=1; row < shape[0]; ++row) {
        for (auto col=1; col < shape[1]; ++col) {
            // this is the general form
            sat[{row,col}] =
                grid[{row,col}] + sat[{row-1,col}] + sat[{row,col-1}] - sat[{row-1,col-1}];
        }
    }

    // verify
    for (const auto & idx : sat.layout()) {
        // the expected value
        double expected = (idx[0]+1) * (idx[1]+1) * value;
        // compare
        assert(( sat[idx] == expected ));
    }

    // all done
    return 0;
}


// end of file
