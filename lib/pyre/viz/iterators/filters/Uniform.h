// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// a filter that maps values in [0,1] onto a the cell index of a uniformly spaced grid
template <class sourceT>
class pyre::viz::iterators::filters::Uniform {
    // types
public:
    // my template parameter
    using source_type = sourceT;
    // and its reference type
    using source_const_reference = const source_type &;
    // my value type
    using value_type = int;

    // metamethods
public:
    // constructor
    inline Uniform(source_const_reference source, int bins);

    // interface
public:
    inline auto operator*() const -> value_type;
    inline auto operator++() -> void;

    // implementation details: data
private:
    source_type _source;
    const double _scale;

    // default metamethods
public:
    // destructor
    ~Uniform() = default;

    // constructors
    Uniform(const Uniform &) = default;
    Uniform(Uniform &&) = default;

    // deleted metamethods
public:
    // because {_bins} is {const}
    Uniform & operator=(const Uniform &) = delete;
    Uniform & operator=(Uniform &&) = delete;
};


// get the inline definitions
#include "Uniform.icc"


// end of file
