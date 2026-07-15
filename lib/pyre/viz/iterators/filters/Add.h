// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"


// a filter that add the values of two others
template <class op1T, class op2T>
class pyre::viz::iterators::filters::Add {
    // types
public:
    // me
    using self_type = Add<op1T, op2T>;
    // my template parameters
    using op1_type = op1T;
    using op2_type = op2T;
    // and their reference types
    using op1_const_reference = const op1_type &;
    using op2_const_reference = const op2_type &;

    // my value type
    using value_type = double;

    // metamethods
public:
    // constructor
    inline Add(op1_const_reference op1, op2_const_reference op2);

    // interface
public:
    inline auto operator*() const;
    inline auto operator++() -> void;

    // implementation details: data
private:
    op1_type _op1;
    op2_type _op2;

    // default metamethods
public:
    // destructor
    ~Add() = default;

    // constructors
    Add(const Add &) = default;
    Add & operator=(const Add &) = default;
    Add(Add &&) = default;
    Add & operator=(Add &&) = default;
};


// get the inline definitions
#include "Add.icc"


// end of file
