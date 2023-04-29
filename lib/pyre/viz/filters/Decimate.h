// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_viz_filters_Decimate_h)
#define pyre_viz_filters_Decimate_h


// a filter that samples its input source at some zoom level by dropping pixels
template <class sourceT>
class pyre::viz::filters::Decimate {
    // types
public:
    // my template parameter
    using source_type = sourceT;
    // and its reference type
    using source_const_reference = const source_type &;

    // packing types
    using packing_type = typename source_type::packing_type;
    // indices
    using index_type = typename source_type::index_type;
    // shapes
    using shape_type = typename source_type::shape_type;

    // my value type
    using value_type = typename source_type::value_type;

    // metamethods
public:
    // constructor
    inline Decimate(
        // the source; expected to be grid-like
        source_const_reference source,
        // the tile spec
        index_type origin, shape_type shape,
        // decimation control, expressed as an index shift
        index_type stride);

    // interface
public:
    inline auto operator*() const -> value_type;
    inline auto operator++() -> void;

    // implementation details: data
private:
    // my source
    source_const_reference _source;
    // my cursor
    typename source_type::index_iterator _cursor;

    // default metamethods
public:
    // destructor
    ~Decimate() = default;

    // constructors
    Decimate(const Decimate &) = default;
    Decimate & operator=(const Decimate &) = default;
    Decimate(Decimate &&) = default;
    Decimate & operator=(Decimate &&) = default;
};


// get the inline definitions
#define pyre_viz_filters_Decimate_icc
#include "Decimate.icc"
#undef pyre_viz_filters_Decimate_icc


#endif

// end of file
