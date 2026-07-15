// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"


// a filter computes the fractional part of the logarithm of its source
template <class sourceT>
class pyre::viz::iterators::filters::PolarSaw {
    // types
public:
    // me
    using self_type = PolarSaw<sourceT>;
    // my template parameter
    using source_type = sourceT;
    // and its reference type
    using source_const_reference = const source_type &;
    // my value type
    using value_type = double;

    // metamethods
public:
    // constructor
    inline PolarSaw(source_const_reference source);

    // interface
public:
    inline auto operator*() const -> value_type;
    inline auto operator++() -> void;

    // implementation details: data
private:
    source_type _source;

    // default metamethods
public:
    // destructor
    ~PolarSaw() = default;

    // constructors
    PolarSaw(const PolarSaw &) = default;
    PolarSaw & operator=(const PolarSaw &) = default;
    PolarSaw(PolarSaw &&) = default;
    PolarSaw & operator=(PolarSaw &&) = default;
};


// get the inline definitions
#include "PolarSaw.icc"


// end of file
