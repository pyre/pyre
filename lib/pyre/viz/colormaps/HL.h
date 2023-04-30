// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_viz_colormaps_HL_h)
#define pyre_viz_colormaps_HL_h


// interpret three input sources as {hue, saturation, luminosity} and generate {rgb_t} color
template <class hueSourceT, class luminositySourceT>
class pyre::viz::colormaps::HL {
    // types
public:
    // my template parameters
    using hue_source_type = hueSourceT;
    using luminosity_source_type = luminositySourceT;
    // and their reference types
    using hue_source_const_reference = const hue_source_type &;
    using luminosity_source_const_reference = const luminosity_source_type &;

    // i generate {r,g,b} triplets
    using rgb_type = viz::rgb_t;

    // metamethods
public:
    inline HL(
        // the sources
        hue_source_const_reference hue, luminosity_source_const_reference luminosity,
        // the free parameters
        double threshold = 0.4);

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
    luminosity_source_type _luminosity;
    double _threshold;

    // default metamethods
public:
    // destructor
    ~HL() = default;

    // constructors
    HL(const HL &) = default;
    HL(HL &&) = default;
    HL & operator=(const HL &) = default;
    HL & operator=(HL &&) = default;
};


// get the inline definitions
#define pyre_viz_colormaps_HL_icc
#include "HL.icc"
#undef pyre_viz_colormaps_HL_icc


#endif

// end of file
