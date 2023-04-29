// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_viz_filters_Cycle_h)
#define pyre_viz_filters_Cycle_h


// a filter that extracts the phase of its complex source as cycle in [0,1]
template <class sourceT>
class pyre::viz::filters::Cycle {
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
    inline Cycle(source_const_reference source, interval_type interval);

    // interface
public:
    inline auto operator*() const -> value_type;
    inline auto operator++() -> void;

    // implementation details: data
private:
    source_type _source;
    interval_type _interval;

    // default metamethods
public:
    // destructor
    ~Cycle() = default;

    // constructors
    Cycle(const Cycle &) = default;
    Cycle & operator=(const Cycle &) = default;
    Cycle(Cycle &&) = default;
    Cycle & operator=(Cycle &&) = default;
};


// get the inline definitions
#define pyre_viz_filters_Cycle_icc
#include "Cycle.icc"
#undef pyre_viz_filters_Cycle_icc


#endif

// end of file
