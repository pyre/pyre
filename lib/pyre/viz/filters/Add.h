// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_viz_filters_Add_h)
#define pyre_viz_filters_Add_h


// a filter that add the values of two others
template <class op1T, class op2T>
class pyre::viz::filters::Add {
    // types
public:
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
#define pyre_viz_filters_Add_icc
#include "Add.icc"
#undef pyre_viz_filters_Add_icc


#endif

// end of file
