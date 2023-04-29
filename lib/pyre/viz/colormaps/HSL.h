// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_viz_colormaps_HSL_h)
#define pyre_viz_colormaps_HSL_h


// interpret three input sources as {hue, saturation, luminosity} and generate {rgb_t} color
template <class hueSourceT, class saturationSourceT, class luminositySourceT>
class pyre::viz::colormaps::HSL {
    // types
public:
    // my template parameters
    using hue_source_type = hueSourceT;
    using saturation_source_type = saturationSourceT;
    using luminosity_source_type = luminositySourceT;
    // and their reference types
    using hue_source_const_reference = const hue_source_type &;
    using saturation_source_const_reference = const saturation_source_type &;
    using luminosity_source_const_reference = const luminosity_source_type &;

    // i generate {r,g,b} triplets
    using rgb_type = viz::rgb_t;

    // metamethods
public:
    inline HSL(
        hue_source_const_reference hue, saturation_source_const_reference saturation,
        luminosity_source_const_reference luminosity);

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
    luminosity_source_type _luminosity;

    // default metamethods
public:
    // destructor
    ~HSL() = default;

    // constructors
    HSL(const HSL &) = default;
    HSL(HSL &&) = default;
    HSL & operator=(const HSL &) = default;
    HSL & operator=(HSL &&) = default;
};


// get the inline definitions
#define pyre_viz_colormaps_HSL_icc
#include "HSL.icc"
#undef pyre_viz_colormaps_HSL_icc


#endif

// end of file
