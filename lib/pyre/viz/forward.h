// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

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
    using byte_t = unsigned char;

    // filters
    namespace filters {
        // a filter that adds two others
        template <class op1T, class op2T>
        class Add;
        // map [0,1] to a portion of an interval
        template <class sourceT>
        class Affine;
        // extract the amplitude of a complex source
        template <class sourceT>
        class Amplitude;
        // supply a constant value
        template <typename valueT>
        class Constant;
        // compute phase as a cycle in [0,1]
        template <typename valueT>
        class Cycle;
        // a simple compressor that just drops pixels
        template <class sourceT>
        class Decimate;
        // a filter that maps values in [0,1] to the index of of a call in a geometrically spaced
        // grid
        template <class sourceT>
        class Geometric;
        // imaginary part of a complex source
        template <class sourceT>
        class Imaginary;
        // a saw tooth function based on the log of its input value
        template <class sourceT>
        class LogSaw;
        // a filter that multiples two others
        template <class op1T, class op2T>
        class Multiply;
        // scale values relative to an interval
        template <class sourceT>
        class Parametric;
        // extract the phase of a complex source
        template <class sourceT>
        class Phase;
        // a saw tooth function based on the phase of its input value
        template <class sourceT>
        class PolarSaw;
        // a power law filter for amplitudes
        template <class sourceT>
        class Power;
        // real part of a complex source
        template <class sourceT>
        class Real;
        // a filter that maps values in [0,1] to the index of of a call in a uniformly spaced grid
        template <class sourceT>
        class Uniform;
    } // namespace filters

    // color maps
    namespace colormaps {
        template <class sourceT>
        class Complex;

        template <class sourceT>
        class Gray;

        template <class hueSourceT, class luminositySourceT>
        class HL;

        template <class hueSourceT, class saturationSourceT, class brightnessSourceT>
        class HSB;

        template <class hueSourceT, class saturationSourceT, class luminositySourceT>
        class HSL;

        template <class redSourceT, class greenSourceT, class blueSourceT>
        class RGB;
    } // namespace colormaps


    // codecs
    // microsoft bitmap
    class BMP;

} // namespace pyre::viz


#endif

// end of file
