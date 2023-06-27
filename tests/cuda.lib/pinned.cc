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
using pinned_t = pyre::cuda::memory::pinned_t<double>;


// main program
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);

    // make a channel
    pyre::journal::debug_t channel("pyre.cuda.memory");

    // pick a number
    const int cells = 1024 * 1024;
    // allocate some memory
    pinned_t arena(cells);

    // show me the address
    channel << "allocated " << cells << " doubles at " << arena.host_data()
            << pyre::journal::endl(__HERE__);

    // verify we can iterate and initialize all cells
    for (int index = 0; index < cells; ++index) {
        // to unity
        arena[index] = 1.0;
    }

    // verify we can iterate and read
    for (int index = 0; index < cells; ++index) {
        // verify the memory contents are what we expect
        assert((arena[index] == 1.0));
    }

    // all done
    return 0;
}

// end of file
