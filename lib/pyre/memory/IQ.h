// -*- c++ -*-
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
// the aliases, for the native form of a count
#include "api.h"


// a radar sample: the in-phase and quadrature counts, as the instrument recorded them
//
// a pair of integers and nothing more: it is built, read and compared, and does no arithmetic,
// so a client that computes with samples makes the values it needs out of the two counts; its
// bytes are the bytes of the two counts back to back, so it lays over memory mapped products
// and over the compound types that store such samples in files
//
// the counts may be byte ordered cells, so a sample stored in the other byte order swaps each
// count on its own: {IQ<foreign_t<std::uint16_t>>}
template <typename T>
class pyre::memory::IQ {
    // the counts must travel byte by byte, or the pair cannot lay over stored samples
    static_assert(std::is_trivially_copyable_v<T>, "the counts of a sample must be trivial");

    // types
public:
    // me
    using self_type = IQ<T>;
    // the type of each count
    using value_type = T;

    // metamethods
public:
    // an indeterminate sample, exactly like the counts it holds
    constexpr IQ() = default;
    // a sample out of its two counts
    constexpr IQ(value_type i, value_type q);
    // the same sample out of counts in another byte order; implicit, the way a byte ordered
    // count accepts its native value, so a sample in the host's order stores into any cell
    template <typename U>
        requires std::same_as<native_t<U>, native_t<T>>
    constexpr IQ(const IQ<U> & other);

    // special members
    constexpr IQ(const IQ &) = default;
    constexpr IQ(IQ &&) = default;
    constexpr IQ & operator=(const IQ &) = default;
    constexpr IQ & operator=(IQ &&) = default;
    ~IQ() = default;

    // data
public:
    // the in-phase count
    value_type i;
    // the quadrature count
    value_type q;
};


// the native form of a sample holds the native form of its counts
template <typename T>
struct pyre::memory::Native<pyre::memory::IQ<T>> {
    // unwrap each count
    using type = IQ<native_t<T>>;
};


// a sample that reads correctly at any address holds counts that do
template <typename T>
struct pyre::memory::Unaligned<pyre::memory::IQ<T>> {
    // wrap each count
    using type = IQ<unaligned_t<T>>;
};


// get the inline definitions
#include "IQ.icc"


// end of file
