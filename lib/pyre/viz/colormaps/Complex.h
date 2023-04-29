// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_viz_colormaps_Complex_h)
#define pyre_viz_colormaps_Complex_h


// map complex values to (hue, brightness)
template <class sourceT>
class pyre::viz::colormaps::Complex {
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
    inline Complex(
        // the data source, most often an iterator over a dataset
        source_const_reference data,
        // color map configuration
        int bins = 32,
        // the amount of color to inject
        double saturation = 0.5,
        // brightness range
        double minBrightness = 0, double maxBrightness = 1,
        // the data space
        double minAmplitude = 0, double maxAmplitude = 1,
        // the colors to use for out of range data
        // by default, underflow maps to black
        rgb_type underflow = { 0, 0, 0 },
        // and overflow to white
        rgb_type overflow = { 1, 1, 1 });

    // interface: pretend to be an iterator
public:
    // map the current data value to a color
    inline auto operator*() const -> rgb_type;
    // get the next value from the source; only support the prefix form, if possible
    inline auto operator++() -> void;

    // implementation details: data
private:
    int _bins;
    double _saturation;
    // hue mapping
    double _scaleHue;
    // brightness mapping
    double _minBrightness, _maxBrightness, _scaleBrightness;
    double _minAmplitude, _maxAmplitude, _scaleAmplitude;
    // out of range values
    rgb_type _overflow;
    rgb_type _underflow;

    // the data source
    // in an earlier implementation, this was a reference to a source_type, an idea that
    // was discarded because it makes branching workflows impossible
    source_type _source;

    // default metamethods
public:
    // destructor
    ~Complex() = default;

    // constructors
    Complex(const Complex &) = default;
    Complex(Complex &&) = default;
    Complex & operator=(const Complex &) = default;
    Complex & operator=(Complex &&) = default;
};


// get the inline definitions
#define pyre_viz_colormaps_Complex_icc
#include "Complex.icc"
#undef pyre_viz_colormaps_Complex_icc


#endif

// end of file
