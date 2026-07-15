// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"


// a filter that always presents a constant value
template <typename valueT>
class pyre::viz::iterators::filters::Constant {
    // types
public:
    // me
    using self_type = Constant<valueT>;
    // my value type
    using value_type = valueT;

    // metamethods
public:
    // constructor
    inline Constant(value_type value);

    // interface
public:
    inline auto operator*() const -> value_type;
    inline auto operator++() const -> void;

    // implementation details: data
private:
    const value_type _value;

    // default metamethods
public:
    // destructor
    ~Constant() = default;

    // constructors
    Constant(const Constant &) = default;
    Constant(Constant &&) = default;

    // deleted metamethods
public:
    // because {_value} is {const}
    Constant & operator=(const Constant &) = delete;
    Constant & operator=(Constant &&) = delete;
};


// get the inline definitions
#include "Constant.icc"


// end of file
