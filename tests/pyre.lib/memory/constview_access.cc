// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the memory
#include <pyre/memory.h>
// support
#include <cassert>


// type alias
using constview_t = pyre::memory::constview_t<double>;


// make a const view over someone else's data
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("constview_access");

    // the number of cells
    std::size_t cells = 1024ul;
    // allocate a memory block
    double * block = new double[cells];
    // initialize
    for (std::size_t pos=0; pos<cells; ++pos) {
        // every cell
        block[pos] = 1.0;
    }

    // use the clock to build a view
    constview_t view(block, cells);

    // verify we can iterate and read
    for (auto cell : view) {
        // check that we have what we expect
        assert(( cell == 1.0 ));
    }

    // exercise operator []
    // read from somewhere
    assert(( view[cells/2] == 1.0 ));

    // clean up; after this, the memory of our view is invalid
    delete [] block;

    // all done
    return 0;
}


// end of file
