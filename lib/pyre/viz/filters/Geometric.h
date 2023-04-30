// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_viz_filters_Geometric_h)
#define pyre_viz_filters_Geometric_h


// a filter that maps values in [0,1] onto a the cell index of a geometric grid
template <class sourceT>
class pyre::viz::filters::Geometric {
    // types
public:
    // my template parameter
    using source_type = sourceT;
    // and its reference type
    using source_const_reference = const source_type &;
    // my value type
    using value_type = int;

    // metamethods
public:
    // destructor
    ~Geometric();

    // constructor
    inline Geometric(source_const_reference source, int bins, double factor);

    // copy/move constructors
    Geometric(const Geometric &);
    Geometric(Geometric &&);

    // interface
public:
    inline auto operator*() const -> value_type;
    inline auto operator++() -> void;

    // implementation details: data
private:
    source_type _source;
    const int _bins;
    const double _scale;
    double * _ticks;

    // deleted metamethods
public:
    // because {_bins} and {_scale} are {const}
    Geometric & operator=(const Geometric &) = delete;
    Geometric & operator=(Geometric &&) = delete;
};


// get the inline definitions
#define pyre_viz_filters_Geometric_icc
#include "Geometric.icc"
#undef pyre_viz_filters_Geometric_icc


#endif

// end of file
