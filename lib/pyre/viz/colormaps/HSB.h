// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_viz_colormaps_HSB_h)
#define pyre_viz_colormaps_HSB_h


// interpret three input sources as {hue, saturation, brightness} and generate {rgb_t} color
template <class hueSourceT, class saturationSourceT, class brightnessSourceT>
class pyre::viz::colormaps::HSB {
    // types
public:
    // my template parameters
    using hue_source_type = hueSourceT;
    using saturation_source_type = saturationSourceT;
    using brightness_source_type = brightnessSourceT;
    // and their reference types
    using hue_source_const_reference = const hue_source_type &;
    using saturation_source_const_reference = const saturation_source_type &;
    using brightness_source_const_reference = const brightness_source_type &;

    // i generate {r,g,b} triplets
    using rgb_type = viz::rgb_t;

    // metamethods
public:
    inline HSB(
        hue_source_const_reference hue, saturation_source_const_reference saturation,
        brightness_source_const_reference brightness);

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
    brightness_source_type _brightness;

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
