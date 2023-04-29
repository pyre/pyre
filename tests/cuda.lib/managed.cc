// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// for the build system
#include <portinfo>
// support
#include <cassert>
// access to the CUDA memory allocators
#include <pyre/cuda/memory.h>
// and the journal
#include <pyre/journal.h>


// type alias
using managed_t = pyre::cuda::memory::managed_t<double>;


// main program
int main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);

    // make a channel
    pyre::journal::debug_t channel("pyre.cuda.memory");

    // pick a number
    const int cells = 1024 * 1024;
    // allocate some memory
    managed_t arena(cells);

    // show me the address
    channel
        << "allocated " << cells << " doubles at " << arena.data()
        << pyre::journal::endl(__HERE__);

    // verify we can iterate and initialize all cells
    for (auto & cell : arena) {
        // to unity
        cell = 1.0;
    }

    // verify we can iterate and read
    for (auto cell : arena) {
        // verify the memory contents are what we expect
        assert(( cell == 1.0 ));
    }

    // all done
    return 0;
}

// end of file
