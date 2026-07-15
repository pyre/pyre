// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"


// a filter that extracts the phase of its complex source
template <class sourceT>
class pyre::viz::iterators::filters::Phase {
    // types
public:
    // me
    using self_type = Phase<sourceT>;
    // my template parameter
    using source_type = sourceT;
    // and its reference type
    using source_const_reference = const source_type &;

    // my value type
    using value_type = double;

    // metamethods
public:
    // constructor
    inline Phase(source_const_reference source);

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
    ~Phase() = default;

    // constructors
    Phase(const Phase &) = default;
    Phase & operator=(const Phase &) = default;
    Phase(Phase &&) = default;
    Phase & operator=(Phase &&) = default;
};


// get the inline definitions
#include "Phase.icc"


// end of file
