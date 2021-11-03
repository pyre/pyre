// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2021 all rights reserved

// code guard
#if !defined(pyre_viz_filters_Constant_h)
#define pyre_viz_filters_Constant_h


// a filter that always presents a constant value
class pyre::viz::filters::Constant {
    // types
public:
    // my value type
    using value_type = double;

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
    Constant & operator=(const Constant &) = default;
    Constant(Constant &&) = default;
    Constant & operator=(Constant &&) = default;
};


// get the inline definitions
#define pyre_viz_filters_Constant_icc
#include "Constant.icc"
#undef pyre_viz_filters_Constant_icc


#endif

// end of file
