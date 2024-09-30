// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

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

    // aliases for the atomic types
    // signed integers
    using i1_t = std::int8_t;
    using i2_t = std::int16_t;
    using i4_t = std::int32_t;
    using i8_t = std::int64_t;
    // unsigned integers
    using u1_t = std::uint8_t;
    using u2_t = std::uint16_t;
    using u4_t = std::uint32_t;
    using u8_t = std::uint64_t;
    // floats
    using f4_t = float;
    using f8_t = double;
    // complex
    using c8_t = std::complex<float>;
    using c16_t = std::complex<double>;

    // products
    namespace products {
        // images
        namespace images {
            // microsoft bitmaps
            class BMP;
        } // namespace images
    }     // namespace products

    // factories
    namespace factories {
        // codecs
        namespace codecs {
            // microsoft bitmaps
            template <class redT, class greenT, class blueT>
            class BMP;
        } // namespace codecs
        // colorspaces
        namespace colormaps {
            // grayscale
            template <class signalT, class redT, class greenT, class blueT>
            class Gray;

            // hue based spaces
            template <class hueT, class luminosityT, class redT, class greenT, class blueT>
            class HL;

            template <
                class hueT, class saturationT, class brightnessT, class redT, class greenT,
                class blueT>
            class HSB;

            template <
                class hueT, class saturationT, class luminosityT, class redT, class greenT,
                class blueT>
            class HSL;

            // a factory for complex inputs
            template <class signalT, class redT, class greenT, class blueT>
            class Complex;
        } // namespace colormaps
        // filters
        namespace filters {
            template <class signalT, class affineT>
            class Affine;

            template <class signalT, class cycleT>
            class Cycle;

            template <class constantT>
            class Constant;

            template <class signalT>
            class Decimate;

            template <class signalT, class binT>
            class Geometric;

            template <class signalT, class logsawT>
            class LogSaw;

            template <class signalT, class parametricT>
            class Parametric;

            template <class signalT, class polarsawT>
            class PolarSaw;

            template <class signalT, class powerT>
            class Power;

            template <class signalT, class binT>
            class Uniform;
        } // namespace filters
        // selectors
        namespace selectors {
            // complex parts
            template <class signalT, class amplitudeT>
            class Amplitude;

            template <class signalT, class imaginaryT>
            class Imaginary;

            template <class signalT, class phaseT>
            class Phase;

            template <class signalT, class realT>
            class Real;
        } // namespace selectors
    }     // namespace factories

    // iterators
    namespace iterators {
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
            // a filter that maps values in [0,1] to the index of of a call in a geometrically
            // spaced grid
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
            // a filter that maps values in [0,1] to the index of of a call in a uniformly spaced
            // grid
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
        namespace codecs {
            // microsoft bitmap
            class BMP;
        } // namespace codecs
    }     // namespace iterators


} // namespace pyre::viz


#endif

// end of file
