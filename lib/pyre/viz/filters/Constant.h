// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_viz_filters_Constant_h)
#define pyre_viz_filters_Constant_h


// a filter that always presents a constant value
template <typename valueT>
class pyre::viz::filters::Constant {
    // types
public:
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
#define pyre_viz_filters_Constant_icc
#include "Constant.icc"
#undef pyre_viz_filters_Constant_icc


#endif

// end of file
