// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the memory
#include <pyre/memory.h>
// support
#include <cassert>


// the pieces under test: a sample in the host's order, and the same sample in the other order
using native_t = pyre::memory::iq_t<pyre::memory::uint16_t>;
using foreign_t = pyre::memory::iq_t<pyre::memory::foreign_t<pyre::memory::uint16_t>>;
// the bytes of one sample
using bytes_t = std::array<std::byte, sizeof(native_t)>;


// the sample in the other order is as wide as the native one and still lays over stored bytes
static_assert(sizeof(foreign_t) == sizeof(native_t));
static_assert(std::is_trivially_copyable_v<foreign_t>);
// its native form is the native sample
static_assert(std::is_same_v<pyre::memory::native_t<foreign_t>, native_t>);
// and a sample that reads at any address keeps each of its counts byte aligned
static_assert(alignof(pyre::memory::unaligned_t<native_t>) == 1);


// verify that a sample stored in the other byte order swaps each count on its own
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("iq_ordered");

    // a sample whose bytes are all distinct
    const native_t sample { 0x0102, 0x0304 };
    // the same sample in the other order
    const foreign_t foreign { sample.i, sample.q };

    // each count reads back as its value
    assert((foreign.i == sample.i));
    assert((foreign.q == sample.q));
    // and converting back to the host's order gives the sample
    assert((native_t { foreign } == sample));
    // as does converting the sample itself into the other order and back
    assert((native_t { foreign_t { sample } } == sample));
    // a sample in the host's order stores into a cell in the other order
    foreign_t cell;
    cell = sample;
    assert((native_t { cell } == sample));

    // in memory, each count has its own bytes reversed, and the counts stay where they were
    auto expected = std::bit_cast<bytes_t>(sample);
    std::reverse(expected.begin(), expected.begin() + 2);
    std::reverse(expected.begin() + 2, expected.end());
    assert((std::bit_cast<bytes_t>(foreign) == expected));

    // all done
    return 0;
}


// end of file
