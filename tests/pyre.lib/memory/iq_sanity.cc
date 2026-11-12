// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the memory
#include <pyre/memory.h>
// support
#include <cassert>


// the piece under test: a sample with two unsigned 16-bit counts
using iq_t = pyre::memory::iq_t<pyre::memory::uint16_t>;


// a sample is the two counts back to back, so it lays over stored samples
static_assert(sizeof(iq_t) == 2 * sizeof(pyre::memory::uint16_t));
static_assert(offsetof(iq_t, i) == 0);
static_assert(offsetof(iq_t, q) == sizeof(pyre::memory::uint16_t));
static_assert(std::is_standard_layout_v<iq_t>);
static_assert(std::is_trivially_copyable_v<iq_t>);
// its native form is itself
static_assert(std::is_same_v<pyre::memory::native_t<iq_t>, iq_t>);


// verify that a sample holds its two counts, compares count by count, and knows its name
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("iq_sanity");

    // make a sample
    const iq_t sample { 3, 4 };
    // it holds its counts
    assert((sample.i == 3));
    assert((sample.q == 4));
    // it equals a sample with the same counts
    assert((sample == iq_t { 3, 4 }));
    // and differs from one with either count changed, or with the counts exchanged
    assert((sample != iq_t { 5, 4 }));
    assert((sample != iq_t { 3, 5 }));
    assert((sample != iq_t { 4, 3 }));

    // samples copy like the counts they hold
    iq_t copy = sample;
    assert((copy == sample));
    // and their counts can be set one at a time
    copy.q = 7;
    assert((copy == iq_t { 3, 7 }));

    // the name of the cell type, used to name its bindings
    assert((pyre::memory::cellname_t<iq_t>::name() == "IQUInt16"));
    // and its spelling in c++
    assert((pyre::memory::cellname_t<iq_t>::decl() == "pyre::memory::iq_t<std::uint16_t>"));

    // all done
    return 0;
}


// end of file
