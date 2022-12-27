// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the memory
#include <pyre/memory.h>
// support
#include <cassert>


// type alias
using view_t = pyre::memory::view_t<double>;


// create a view over a foreign block of data
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("view_access");

    // the number of cells
    std::size_t cells = 1024ul;
    // allocate a memory block
    double * block = new double[cells];

    // convert it into a view
    view_t view(block, cells);

    // verify we can iterate and write
    for (auto & cell : view) {
        // to zero
        cell = 0;
    }

    // verify we can iterate and read
    for (auto cell : view) {
        // check that we have what we expect
        assert(( cell == 0 ));
    }

    // exercise operator []
    // write
    view[cells/2] = 1;
    // and read
    assert(( view[cells/2] == 1 ));

    // clean up
    delete [] block;

    // all done
    return 0;
}


// end of file
