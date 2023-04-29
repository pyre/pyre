// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_viz_filters_Parametric_h)
#define pyre_viz_filters_Parametric_h


// a filter that shifts and scales its input values based on a given interval
template <class sourceT>
class pyre::viz::filters::Parametric {
    // types
public:
    // my template parameter
    using source_type = sourceT;
    // and its reference type
    using source_const_reference = const source_type &;
    // my value type
    using value_type = double;
    // my interval
    using interval_type = interval_t;

    // metamethods
public:
    // constructor
    inline Parametric(source_const_reference source, interval_type interval);

    // interface
public:
    inline auto operator*() const -> value_type;
    inline auto operator++() -> void;

    // implementation details: data
private:
    source_type _source;
    const interval_type _interval;

    // default metamethods
public:
    // destructor
    ~Parametric() = default;

    // constructors
    Parametric(const Parametric &) = default;
    Parametric(Parametric &&) = default;

    // deleted metamethods
public:
    // because {_interval} is {const}
    Parametric & operator=(const Parametric &) = delete;
    Parametric & operator=(Parametric &&) = delete;
};


// get the inline definitions
#define pyre_viz_filters_Parametric_icc
#include "Parametric.icc"
#undef pyre_viz_filters_Parametric_icc


#endif

// end of file
