// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_viz_filters_Multiply_h)
#define pyre_viz_filters_Multiply_h


// a filter that multiplies the values of two others
template <class op1T, class op2T>
class pyre::viz::filters::Multiply {
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
    inline Multiply(op1_const_reference op1, op2_const_reference op2);

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
    ~Multiply() = default;

    // constructors
    Multiply(const Multiply &) = default;
    Multiply & operator=(const Multiply &) = default;
    Multiply(Multiply &&) = default;
    Multiply & operator=(Multiply &&) = default;
};


// get the inline definitions
#define pyre_viz_filters_Multiply_icc
#include "Multiply.icc"
#undef pyre_viz_filters_Multiply_icc


#endif

// end of file
