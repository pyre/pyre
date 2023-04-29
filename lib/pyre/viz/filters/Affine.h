// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_viz_filters_Affine_h)
#define pyre_viz_filters_Affine_h


// map [0,1] to a portion of an interval
template <class sourceT>
class pyre::viz::filters::Affine {
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
    inline Affine(source_const_reference source, interval_type interval);

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
    ~Affine() = default;

    // constructors
    Affine(const Affine &) = default;
    Affine(Affine &&) = default;

    // deleted metamethods
public:
    // because {_interval} is {const}
    Affine & operator=(const Affine &) = delete;
    Affine & operator=(Affine &&) = delete;
};


// get the inline definitions
#define pyre_viz_filters_Affine_icc
#include "Affine.icc"
#undef pyre_viz_filters_Affine_icc


#endif

// end of file
