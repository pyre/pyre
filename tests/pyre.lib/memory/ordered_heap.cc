// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the memory
#include <pyre/memory.h>
// support
#include <cassert>


// the pieces under test: a heap block of scalars in the order the host lacks
using value_t = pyre::memory::int32_t;
using cell_t = pyre::memory::foreign_t<value_t>;
using heap_t = pyre::memory::heap_t<cell_t>;
// and the bytes of one cell
using bytes_t = std::array<std::byte, sizeof(value_t)>;


// verify that a memory block over byte ordered cells reads and writes native values while
// keeping its bytes in the declared order
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("ordered_heap");

    // the number of cells
    const std::size_t cells = 256ul;
    // make a block on the heap
    heap_t block(cells);
    // the block is as wide as the same number of native scalars
    assert((block.bytes() == cells * sizeof(value_t)));

    // stamp every cell with its own offset, as a native value
    value_t offset = 0;
    for (auto & cell : block) {
        // through the wrapper
        cell = offset++;
    }

    // read them all back
    offset = 0;
    for (auto cell : block) {
        // each cell must hold the native value it was given
        assert((cell == offset++));
    }

    // look at the raw bytes of a cell: they are the native bytes, reversed
    const value_t sample = 0x0a0b0c0d;
    block[cells / 2] = sample;
    auto expected = std::bit_cast<bytes_t>(sample);
    std::reverse(expected.begin(), expected.end());
    assert((std::bit_cast<bytes_t>(block.data()[cells / 2]) == expected));
    // while the cell itself reads as the native value
    assert((block[cells / 2] == sample));

    // fill the whole block with one value
    block.fill(-17);
    // and check
    for (auto cell : block) {
        // every cell agrees
        assert((cell == -17));
    }

    // all done
    return 0;
}


// end of file
