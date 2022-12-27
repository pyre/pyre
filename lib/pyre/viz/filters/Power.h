// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_viz_filters_Power_h)
#define pyre_viz_filters_Power_h


// a filter computes the fractional part of the logarithm of its source
template <class sourceT>
class pyre::viz::filters::Power {
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
    inline Power(source_const_reference source, double mean, double scale, double exponent);

    // interface
public:
    inline auto operator*() const -> value_type;
    inline auto operator++() -> void;

    // implementation details: data
private:
    // the source
    source_type _source;
    // the parameters
    double _mean;
    double _scale;
    double _exponent;

    // default metamethods
public:
    // destructor
    ~Power() = default;

    // constructors
    Power(const Power &) = default;
    Power & operator=(const Power &) = default;
    Power(Power &&) = default;
    Power & operator=(Power &&) = default;
};


// get the inline definitions
#define pyre_viz_filters_Power_icc
#include "Power.icc"
#undef pyre_viz_filters_Power_icc


#endif

// end of file
