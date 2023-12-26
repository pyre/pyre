// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_viz_api_h)
#define pyre_viz_api_h


// publicly visible types
namespace pyre::viz {
    // correctly typed file streams for reading and writing to avoid having to cast
    // {byte_t *} to {char *}
    // using fstream_t = std::basic_fstream<byte_t>;
    // using ifstream_t = std::basic_ifstream<byte_t>;
    // using ofstream_t = std::basic_ofstream<byte_t>;
    // N.B. these used to be aliases to {std::?stream<byte_t>} but the llvm libc++ seems to have
    //      trouble building streams over {unsigned char}
    // LAST CHECKED: 20220502 with llvm-13:
    //      implicit instantiation of undefined template std::codecvt<unsigned char, ...>
    // LAST CHECKED: 20231201 with macports llvm-17
    //      seems to work; must verify i'm linking against libc++
    using fstream_t = std::fstream;
    using ifstream_t = std::ifstream;
    using ofstream_t = std::ofstream;
} // namespace pyre::viz


// products
// memory
namespace pyre::viz::products::memory {
    // atoms
    // signed integers
    using i1_t = I1;
    using i2_t = I2;
    using i4_t = I4;
    using i8_t = I8;
    // unsigned integers
    using u1_t = U1;
    using u2_t = U2;
    using u4_t = U4;
    using u8_t = U8;
    // floats
    using f4_t = F4;
    using f8_t = F8;
    // complex
    using c8_t = C8;
    using c16_t = C16;

    // tiles
    // generic
    template <class packingT, class storageT>
    using tile_t = Tile<packingT, storageT>;
    // signed integers
    using tile_i1_t = TileI1;
    using tile_i2_t = TileI2;
    using tile_i4_t = TileI4;
    using tile_i8_t = TileI8;
    // unsigned integers
    using tile_u1_t = TileU1;
    using tile_u2_t = TileU2;
    using tile_u4_t = TileU4;
    using tile_u8_t = TileU8;
    // floats
    using tile_f4_t = TileF4;
    using tile_f8_t = TileF8;
    // complex
    using tile_c8_t = TileC8;
    using tile_c16_t = TileC16;
} // namespace pyre::viz::products::memory

// images
namespace pyre::viz::products::images {
    // microsoft bitmaps
    using bmp_t = BMP;
} // namespace pyre::viz::products::images


// factories
// codecs
namespace pyre::viz::factories::codecs {
    // microsoft bitmaps
    template <class redT, class greenT = redT, class blueT = redT>
    using bmp_t = BMP<redT, greenT, blueT>;
} // namespace pyre::viz::factories::codecs

// colorspaces
namespace pyre::viz::factories::colormaps {
    // grayscale
    template <class signalT, class redT = signalT, class greenT = redT, class blueT = redT>
    using gray_t = Gray<signalT, redT, greenT, blueT>;

    // hue based spaces
    template <
        class hueT, class luminosityT = hueT, class redT = hueT, class greenT = hueT,
        class blueT = hueT>
    using hl_t = HL<hueT, luminosityT, redT, greenT, blueT>;

    template <
        class hueT, class saturationT = hueT, class brightnessT = hueT, class redT = hueT,
        class greenT = hueT, class blueT = hueT>
    using hsb_t = HSB<hueT, saturationT, brightnessT, redT, greenT, blueT>;

    template <
        class hueT, class saturationT = hueT, class luminosityT = hueT, class redT = hueT,
        class greenT = hueT, class blueT = hueT>
    using hsl_t = HSL<hueT, saturationT, luminosityT, redT, greenT, blueT>;

    // complex data
    template <class signalT, class redT, class greenT = redT, class blueT = redT>
    using complex_t = Complex<signalT, redT, greenT, blueT>;
} // namespace pyre::viz::factories::colormaps

// filters
namespace pyre::viz::factories::filters {
    template <class tileT>
    using constant_t = Constant<tileT>;
}

// selectors
namespace pyre::viz::factories::selectors {
    // complex parts
    template <class signalT, class amplitudeT>
    using amplitude_t = Amplitude<signalT, amplitudeT>;

    using imaginary_t = Imaginary;
    using phase_t = Phase;
    using real_t = Real;
} // namespace pyre::viz::factories::selectors


// conversions from other color spaces to {rgb}
namespace pyre::viz::colorspaces {
    inline auto hl(double h, double l, double threshold = 0.4) -> rgb_t;
    inline auto hsb(double h, double s, double b) -> rgb_t;
    inline auto hsl(double h, double s, double l) -> rgb_t;
} // namespace pyre::viz::colorspaces


// iterators
// codecs
namespace pyre::viz::iterators::codecs {
    // microsoft bmp
    using bmp_t = BMP;
} // namespace pyre::viz::iterators::codecs

// filters
namespace pyre::viz::iterators::filters {
    // a filter that adds two others
    template <class op1T, class op2T>
    using add_t = Add<op1T, op2T>;
    // map a [0,1] interval into a portion of an interval
    template <class sourceT>
    using affine_t = Affine<sourceT>;
    // extract the amplitude of a complex dataset
    template <class sourceT>
    using amplitude_t = Amplitude<sourceT>;
    // supply a constant value
    template <typename valueT = double>
    using constant_t = Constant<valueT>;
    // compute phase as a cycle in [0,1]
    template <typename valueT = double>
    using cycle_t = Cycle<valueT>;
    // a simple compressor that just drops pixels
    template <class sourceT>
    using decimate_t = Decimate<sourceT>;
    // a filter that maps values in [0,1] to the index of of a call in a geometrically spaced grid
    template <class sourceT>
    using geometric_t = Geometric<sourceT>;
    // extract the imaginary part of a complex dataset
    template <class sourceT>
    using imaginary_t = Imaginary<sourceT>;
    // a saw tooth function on the log of its input value
    template <class sourceT>
    using logsaw_t = LogSaw<sourceT>;
    // a filter that multiplies two others
    template <class op1T, class op2T>
    using mul_t = Multiply<op1T, op2T>;
    // scale values relative to a given interval
    template <class sourceT>
    using parametric_t = Parametric<sourceT>;
    // extract the phase of a complex dataset
    template <class sourceT>
    using phase_t = Phase<sourceT>;
    // a saw tooth function on the phase of its input value
    template <class sourceT>
    using polarsaw_t = PolarSaw<sourceT>;
    // a power law filter for signal amplitudes
    template <class sourceT>
    using power_t = Power<sourceT>;
    // extract the real part of a complex dataset
    template <class sourceT>
    using real_t = Real<sourceT>;
    // a saw tooth function on the phase of its input value
    // a filter that maps values in [0,1] to the index of of a call in a uniformly spaced grid
    template <class sourceT>
    using uniform_t = Uniform<sourceT>;
} // namespace pyre::viz::iterators::filters

// color maps
namespace pyre::viz::iterators::colormaps {
    template <class sourceT>
    using complex_t = Complex<sourceT>;

    template <class sourceT>
    using gray_t = Gray<sourceT>;

    template <class hueSourceT, class saturationSourceT, class brightnessSourceT>
    using hsb_t = HSB<hueSourceT, saturationSourceT, brightnessSourceT>;

    template <class hueSourceT, class luminositySourceT>
    using hl_t = HL<hueSourceT, luminositySourceT>;

    template <class hueSourceT, class saturationSourceT, class luminositySourceT>
    using hsl_t = HSB<hueSourceT, saturationSourceT, luminositySourceT>;

    template <class redSourceT, class greenSourceT, class blueSourceT>
    using rgb_t = RGB<redSourceT, greenSourceT, blueSourceT>;
} // namespace pyre::viz::iterators::colormaps


#endif

// end of file
