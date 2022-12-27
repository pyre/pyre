// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the memory
#include <pyre/memory.h>
// support
#include <cassert>


// type alias
using heap_t = pyre::memory::heap_t<double>;


// verify that we can construct and use heap blocks
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("heap_access");

    // the number of cells
    std::size_t cells = 1024ul;
    // make a block on the heap
    heap_t block(cells);

    // verify we can iterate and initialize all cells
    for (auto & cell : block) {
        // to unity
        cell = 1.0;
    }

    // verify we can iterate and read
    for (auto cell : block) {
        // check that we have what we expect
        assert(( cell == 1.0 ));
    }

    // exercise operator []
    // write
    block[cells/2] = 2.0;
    // and read
    assert(( block[cells/2] == 2.0 ));

    // all done
    return 0;
}


// end of file
