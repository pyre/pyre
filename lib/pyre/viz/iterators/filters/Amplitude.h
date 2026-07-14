// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// a filter that extracts the amplitude of its complex data source
template <class sourceT>
class pyre::viz::iterators::filters::Amplitude {
    // types
public:
    // my template parameter
    using source_type = sourceT;
    // and its reference type
    using source_const_reference = const source_type &;

    // my value type
    using value_type = double;

    // metamethods
public:
    // constructor
    inline Amplitude(source_const_reference source);

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
    ~Amplitude() = default;

    // constructors
    Amplitude(const Amplitude &) = default;
    Amplitude & operator=(const Amplitude &) = default;
    Amplitude(Amplitude &&) = default;
    Amplitude & operator=(Amplitude &&) = default;
};


// get the inline definitions
#include "Amplitude.icc"


// end of file
