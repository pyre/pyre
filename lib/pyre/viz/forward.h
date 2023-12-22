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
        // memory
        namespace memory {
            // atoms
            // signed integers
            class I1;
            class I2;
            class I4;
            class I8;
            // unsigned integers
            class U1;
            class U2;
            class U4;
            class U8;
            // floats
            class F4;
            class F8;
            // complex
            class C8;
            class C16;

            // tiles
            // signed integers
            class TileI1;
            class TileI2;
            class TileI4;
            class TileI8;
            // unsigned integers
            class TileU1;
            class TileU2;
            class TileU4;
            class TileU8;
            // floats
            class TileF4;
            class TileF8;
            // complex
            class TileC8;
            class TileC16;
        } // namespace memory
        // images
        namespace images {
            // microsoft bitmaps
            class BMP;
        } // namespace images
    }     // namespace products

    // factories
    namespace factories {
        // arithmetic
        namespace arithmetic {
            // operators
            class AddI1;
        } // namespace arithmetic
        // codecs
        namespace codecs {
            // microsoft bitmaps
            class BMP;
        } // namespace codecs
        // colorspaces
        namespace colorspaces {
            // grayscale
            class Gray;
        } // namespace colorspaces
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
