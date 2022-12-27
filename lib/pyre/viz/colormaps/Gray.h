// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_viz_colormaps_Gray_h)
#define pyre_viz_colormaps_Gray_h


// map a single value to a shade of gray
template <class sourceT>
class pyre::viz::colormaps::Gray {
    // types
public:
    // my template parameter
    using source_type = sourceT;
    // and its reference type
    using source_const_reference = const source_type &;

    // i generate {r,g,b} triplets
    using rgb_type = viz::rgb_t;

    // metamethods
public:
    inline Gray(source_const_reference data);

    // interface: pretend to be an iterator
public:
    // map the current data value to a color
    inline auto operator*() const -> rgb_type;
    // get the next value from the source; only support the prefix form, if possible
    inline auto operator++() -> void;

    // implementation details: data
private:
    // the data source
    source_type _source;

    // default metamethods
public:
    // destructor
    ~Gray() = default;

    // constructors
    Gray(const Gray &) = default;
    Gray(Gray &&) = default;
    Gray & operator=(const Gray &) = default;
    Gray & operator=(Gray &&) = default;
};


// get the inline definitions
#define pyre_viz_colormaps_Gray_icc
#include "Gray.icc"
#undef pyre_viz_colormaps_Gray_icc


#endif

// end of file
