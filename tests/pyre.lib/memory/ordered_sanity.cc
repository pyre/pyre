// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// get the memory
#include <pyre/memory.h>
// support
#include <cassert>


// the pieces under test: a scalar in each explicit byte order, and in the order the host lacks
using big_t = pyre::memory::big_t<pyre::memory::uint32_t>;
using little_t = pyre::memory::little_t<pyre::memory::uint32_t>;
using foreign_t = pyre::memory::foreign_t<pyre::memory::uint32_t>;
// the bytes of one such scalar
using bytes_t = std::array<std::byte, sizeof(pyre::memory::uint32_t)>;


// the spelling that matches the host is the plain scalar, so only the other one is a wrapper
static_assert(std::is_same_v<
              pyre::memory::ordered_t<pyre::memory::uint32_t, std::endian::native>,
              pyre::memory::uint32_t>);
static_assert(!std::is_same_v<foreign_t, pyre::memory::uint32_t>);
// single byte scalars have no order, so they never get wrapped
static_assert(std::is_same_v<pyre::memory::big_t<pyre::memory::uint8_t>, pyre::memory::uint8_t>);
static_assert(std::is_same_v<pyre::memory::little_t<pyre::memory::int8_t>, pyre::memory::int8_t>);
// the wrapper is exactly as wide as the scalar and travels byte by byte
static_assert(sizeof(foreign_t) == sizeof(pyre::memory::uint32_t));
static_assert(std::is_trivially_copyable_v<foreign_t>);
// and the native scalar behind each spelling is the same
static_assert(std::is_same_v<pyre::memory::native_t<foreign_t>, pyre::memory::uint32_t>);
static_assert(
    std::is_same_v<pyre::memory::native_t<pyre::memory::uint32_t>, pyre::memory::uint32_t>);


// verify that a byte ordered scalar stores its bytes in the declared order and reads back as
// the native value
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("ordered_sanity");

    // a value whose bytes are all distinct
    const pyre::memory::uint32_t value = 0x01020304;

    // the same value in each explicit order
    const big_t big = value;
    const little_t little = value;
    // both read back as the value
    assert((big == value));
    assert((little == value));
    // and their bytes sit in memory in the declared order, whatever the host
    assert(
        (std::bit_cast<bytes_t>(big)
         == bytes_t { std::byte { 1 }, std::byte { 2 }, std::byte { 3 }, std::byte { 4 } }));
    assert(
        (std::bit_cast<bytes_t>(little)
         == bytes_t { std::byte { 4 }, std::byte { 3 }, std::byte { 2 }, std::byte { 1 } }));

    // the foreign spelling is a wrapper; exercise its interface
    foreign_t foreign = value;
    // it knows it is not in the host's order
    assert((!foreign.native()));
    // it holds one scalar
    assert((foreign.components() == 1));
    // it reads back as the value, both implicitly and explicitly
    assert((foreign == value));
    assert((foreign.value() == value));
    // and its bytes are the host's bytes, reversed
    auto native = std::bit_cast<bytes_t>(value);
    std::reverse(native.begin(), native.end());
    assert((foreign.bytes() == native));

    // assignment from a native value
    foreign = 7;
    assert((foreign == 7u));
    // compound assignment goes through the native value
    foreign += 3;
    assert((foreign == 10u));
    foreign -= 4;
    assert((foreign == 6u));
    foreign *= 5;
    assert((foreign == 30u));
    foreign /= 3;
    assert((foreign == 10u));
    // and arithmetic in an expression sees the native value
    assert((foreign * 2 == 20u));

    // copies compare equal to each other
    const foreign_t copy = foreign;
    assert((copy == foreign));

    // all done
    return 0;
}


// end of file
