// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the memory
#include <pyre/memory.h>
// support
#include <cassert>


// the pieces under test: a complex scalar in the order the host lacks
using complex_t = pyre::memory::complex64_t;
using foreign_t = pyre::memory::foreign_t<complex_t>;
// the bytes of one component
using component_t = std::array<std::byte, sizeof(float)>;
// and of the whole value
using bytes_t = std::array<std::byte, sizeof(complex_t)>;


// verify that a byte ordered complex scalar swaps each component on its own, never the pair as
// a whole
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("ordered_complex");

    // a value with distinguishable parts
    const complex_t value { 1.5f, -2.0f };
    // in the foreign order
    const foreign_t foreign = value;

    // it knows it holds two scalars
    assert((foreign.components() == 2));
    // it reads back as the value
    assert((foreign == value));
    assert((foreign.value() == value));
    // and casting it makes the native arithmetic available
    assert((static_cast<complex_t>(foreign) * 2.0f == complex_t(3.0f, -4.0f)));

    // the expected byte layout: each component's native bytes, reversed, in the original order
    auto real = std::bit_cast<component_t>(value.real());
    auto imag = std::bit_cast<component_t>(value.imag());
    std::reverse(real.begin(), real.end());
    std::reverse(imag.begin(), imag.end());
    // assemble
    bytes_t expected;
    std::copy(real.begin(), real.end(), expected.begin());
    std::copy(imag.begin(), imag.end(), expected.begin() + real.size());
    // compare
    assert((foreign.bytes() == expected));

    // writes go through the same path
    foreign_t other;
    other = complex_t { 0.25f, 4.0f };
    assert((other == complex_t(0.25f, 4.0f)));
    // as does compound assignment
    other += complex_t { 1.0f, 1.0f };
    assert((other == complex_t(1.25f, 5.0f)));

    // all done
    return 0;
}


// end of file
