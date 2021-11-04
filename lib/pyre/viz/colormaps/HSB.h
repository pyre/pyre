// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2021 all rights reserved

// code guard
#if !defined(pyre_viz_colormaps_HSB_h)
#define pyre_viz_colormaps_HSB_h


// map complex values to (hue, brightness)
template <class hueSourceT, class saturationSourceT, class valueSourceT>
class pyre::viz::colormaps::HSB {
    // types
public:
    // my template parameters
    using hue_source_type = hueSourceT;
    using saturation_source_type = saturationSourceT;
    using value_source_type = valueSourceT;
    // and their reference types
    using hue_source_const_reference = const hue_source_type &;
    using saturation_source_const_reference = const saturation_source_type &;
    using value_source_const_reference = const value_source_type &;

    // individual color values are one byte wide
    using color_type = color_t;
    // i generate {r,g,b} triplets
    using rgb_type = rgb_t;

    // metamethods
public:
    inline HSB(
        hue_source_const_reference hue, saturation_source_const_reference saturation,
        value_source_const_reference value);

    // interface: pretend to be an iterator
public:
    // map the current data value to a color
    inline auto operator*() const -> rgb_type;
    // get the next value from the source; only support the prefix form, if possible
    inline auto operator++() -> void;

    // implementation details: data
private:
    // the data source
    hue_source_type _hue;
    saturation_source_type _saturation;
    value_source_type _value;

    // default metamethods
public:
    // destructor
    ~HSB() = default;

    // constructors
    HSB(const HSB &) = default;
    HSB(HSB &&) = default;
    HSB & operator=(const HSB &) = default;
    HSB & operator=(HSB &&) = default;
};


// get the inline definitions
#define pyre_viz_colormaps_HSB_icc
#include "HSB.icc"
#undef pyre_viz_colormaps_HSB_icc


#endif

// end of file
