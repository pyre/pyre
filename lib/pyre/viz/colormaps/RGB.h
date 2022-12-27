// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_viz_colormaps_RGB_h)
#define pyre_viz_colormaps_RGB_h


// map three color sources to {rgb_t}
template <class redSourceT, class greenSourceT, class blueSourceT>
class pyre::viz::colormaps::RGB {
    // types
public:
    // my template parameters
    using red_source_type = redSourceT;
    using green_source_type = greenSourceT;
    using blue_source_type = blueSourceT;
    // and their reference type
    using red_source_const_reference = const red_source_type &;
    using green_source_const_reference = const green_source_type &;
    using blue_source_const_reference = const blue_source_type &;

    // individual color values are one byte wide
    using color_type = color_t;
    // i generate {r,g,b} triplets
    using rgb_type = viz::rgb_t;

    // metamethods
public:
    inline RGB(
        red_source_const_reference red, green_source_const_reference green,
        blue_source_const_reference blue);

    // interface: pretend to be an iterator
public:
    // map the current data value to a color
    inline auto operator*() const -> rgb_type;
    // get the next value from the source; only support the prefix form, if possible
    inline auto operator++() -> void;

    // implementation details: data
private:
    // the data source
    red_source_type _red;
    green_source_type _green;
    blue_source_type _blue;

    // default metamethods
public:
    // destructor
    ~RGB() = default;

    // constructors
    RGB(const RGB &) = default;
    RGB(RGB &&) = default;
    RGB & operator=(const RGB &) = default;
    RGB & operator=(RGB &&) = default;
};


// get the inline definitions
#define pyre_viz_colormaps_RGB_icc
#include "RGB.icc"
#undef pyre_viz_colormaps_RGB_icc


#endif

// end of file
