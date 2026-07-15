// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// to get std::abs
#include <cstdlib>

namespace pyre::algebra {
    template <size_t scale, typename precisionT = size_t>
    class BCD;
} // namespace pyre::algebra


// global arithmetic operators
// binary +
template <size_t scale, typename precisionT>
pyre::algebra::BCD<scale, precisionT>
operator+(
    const pyre::algebra::BCD<scale, precisionT> &, const pyre::algebra::BCD<scale, precisionT> &);


// binary -
template <size_t scale, typename precisionT>
pyre::algebra::BCD<scale, precisionT>
operator-(
    const pyre::algebra::BCD<scale, precisionT> &, const pyre::algebra::BCD<scale, precisionT> &);


// the BCD class
template <size_t scale, typename precisionT>
class pyre::algebra::BCD {
    // type aliases
public:
    // me
    using self_type = BCD<scale, precisionT>;
    // my parts
    using precision_type = precisionT;

    // interface
public:
    // convert to double
    operator double() const;

    // arithmetic
    BCD operator+() const;
    BCD operator-() const;
    BCD & operator+=(const BCD &);
    BCD & operator-=(const BCD &);

    // meta methods
public:
    // destructor
    ~BCD() = default;

    // constructor
    inline BCD(precision_type msw = 0, precision_type lsw = 0);

    inline BCD(const BCD &) = default;
    inline self_type & operator=(const BCD &) = default;
    inline BCD(BCD &&) = default;
    inline self_type & operator=(BCD &&) = default;

    // data members
public:
    precision_type _msw;
    precision_type _lsw;

    static const size_t _scale = scale;
};


// get the inline definitions
#include "BCD.icc"


// end of file
