// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2021 all rights reserved

// code guard
#if !defined(pyre_viz_forward_h)
#define pyre_viz_forward_h


// set up the namespace
namespace pyre::viz {

    // an interval is a pair of
    using interval_t = std::tuple<double, double>;
    // individual color values are floats in [0,1]
    using color_t = float;
    // {r,g,b} triplets
    using rgb_t = std::tuple<color_t, color_t, color_t>;
    // just to make sure we are all on the same page, wherever it matters
    using byte_t = char;

    // filters
    namespace filters {
        // extract the amplitude of a complex source
        template <class sourceT>
        class Amplitude;
        // supply a constant value
        class Constant;
        // scale values relative to an interval
        template <class sourceT>
        class Parametric;
        // extract the phase of a complex source
        template <class sourceT>
        class Phase;
    } // namespace filters

    // color maps
    namespace colormaps {
        template <class sourceT>
        class Complex;

        template <class sourceT>
        class Gray;

        template <class hueSourceT, class saturationSourceT, class brightnessSourceT>
        class HSB;

        template <class hueSourceT, class saturationSourceT, class luminositySourceT>
        class HSL;

        template <class redSourceT, class greenSourceT, class blueSourceT>
        class RGB;
    } // namespace colormaps


    // codecs
    // micorosoft bitmap
    class BMP;

} // namespace pyre::viz


#endif

// end of file
