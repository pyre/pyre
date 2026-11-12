// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the memory
#include <pyre/memory.h>
// support
#include <cassert>


// the pieces under test: a sample, and a block of them on the heap
using iq_t = pyre::memory::iq_t<pyre::memory::int16_t>;
using heap_t = pyre::memory::heap_t<iq_t>;


// verify that samples are cells like any other: a heap block holds them, and they are written
// and read through it
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("iq_heap");

    // the number of cells
    std::size_t cells = 1024ul;
    // make a block of samples on the heap
    heap_t block(cells);

    // the sample that records a position, with a negative quadrature count
    auto sample = [](std::size_t idx) -> iq_t {
        // the position as a count
        auto count = static_cast<std::int16_t>(idx);
        // and the sample made out of it
        return iq_t { count, static_cast<std::int16_t>(-count) };
    };

    // give each cell its sample
    for (std::size_t idx = 0; idx < cells; ++idx) {
        // write
        block[idx] = sample(idx);
    }

    // verify that each cell reads back as written
    for (std::size_t idx = 0; idx < cells; ++idx) {
        // read and compare
        assert((block[idx] == sample(idx)));
    }

    // a block is a run of samples back to back, each one the two counts in order
    auto counts = reinterpret_cast<const std::int16_t *>(block.data());
    assert((counts[2 * 5] == 5 && counts[2 * 5 + 1] == -5));

    // all done
    return 0;
}


// end of file
