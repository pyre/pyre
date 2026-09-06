// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// externals
#include "externals.h"
// forward declarations
#include "forward.h"


// a scalar whose bytes sit in memory in a fixed byte order, whatever the host's
//
// a cell of this type reads as the native scalar and accepts one on assignment, swapping bytes
// on the way through, so a grid over foreign-order data works cell for cell like a native one;
// it is trivially copyable and exactly as wide as the scalar it stands in for, so it can lay
// over memory mapped files and travel through {std::memset} and friends unharmed
//
// you rarely spell this class out: {ordered_t} in api.h collapses to the plain scalar when the
// requested order is the host's, so only cells that actually need swapping pay for the wrapper
template <typename T, std::endian order>
class pyre::memory::Ordered {
    // the host must be one or the other; mixed-endian machines have no place to stand
    static_assert(
        std::endian::native == std::endian::big || std::endian::native == std::endian::little,
        "byte ordered cells require a big or little endian host");
    // and the scalar must be copyable byte by byte, or the swap makes no sense
    static_assert(std::is_trivially_copyable_v<T>, "byte ordered cells wrap trivial scalars");

    // types
public:
    // me
    using self_type = Ordered<T, order>;
    // the native scalar i stand in for
    using value_type = T;
    // my bytes, exactly as they sit in memory
    using bytes_type = std::array<std::byte, sizeof(T)>;
    // sizes of things
    using size_type = size_t;

    // metamethods
public:
    // an indeterminate value, exactly like the scalar i stand in for
    constexpr Ordered() = default;
    // adopt a native value, storing its bytes in my order
    constexpr Ordered(value_type value);

    // special members
    constexpr Ordered(const Ordered &) = default;
    constexpr Ordered(Ordered &&) = default;
    constexpr Ordered & operator=(const Ordered &) = default;
    constexpr Ordered & operator=(Ordered &&) = default;
    ~Ordered() = default;

    // operators
public:
    // read as the native value
    constexpr operator value_type() const;
    // accept a native value
    constexpr auto operator=(value_type value) -> self_type &;
    // compound assignment, through the native value
    constexpr auto operator+=(value_type value) -> self_type &;
    constexpr auto operator-=(value_type value) -> self_type &;
    constexpr auto operator*=(value_type value) -> self_type &;
    constexpr auto operator/=(value_type value) -> self_type &;

    // interface
public:
    // the byte order of my storage
    static constexpr auto endianness() -> std::endian;
    // whether my bytes happen to be in the host's order
    static constexpr auto native() -> bool;
    // the number of independently ordered scalars i hold: two for complex, one otherwise
    static constexpr auto components() -> size_type;
    // my value in the host's order
    constexpr auto value() const -> value_type;
    // my bytes as they sit in memory
    constexpr auto bytes() const -> bytes_type;

    // implementation details
private:
    // convert a native value to my byte order
    static constexpr auto encode(value_type value) -> bytes_type;
    // convert bytes in my order to a native value
    static constexpr auto decode(bytes_type bytes) -> value_type;
    // reverse the bytes of each component, which is what takes a value between the two orders
    static constexpr auto swap(bytes_type bytes) -> bytes_type;

    // data
private:
    // the value, in my byte order
    bytes_type _bytes;
};


// the native scalar behind a cell value type
// the general case: a type is its own native scalar
template <typename T>
struct pyre::memory::Native {
    // easy
    using type = T;
};

// and the ordered wrapper stands in for the scalar it wraps
template <typename T, std::endian order>
struct pyre::memory::Native<pyre::memory::Ordered<T, order>> {
    // unwrap
    using type = T;
};


// get the inline definitions
#include "Ordered.icc"


// end of file
