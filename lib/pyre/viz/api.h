// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_viz_api_h)
#define pyre_viz_api_h


// publicly visible types
namespace pyre::viz {

    // codecs
    // microsoft bmp
    using bmp_t = BMP;

    // and correctly typed file streams for reading and writing to avaoid having to cast
    // {byte_t *} to {char *}
    // using fstream_t = std::basic_fstream<byte_t>;
    // using ifstream_t = std::basic_ifstream<byte_t>;
    // using ofstream_t = std::basic_ofstream<byte_t>;
    // N.B. these used to be aliases to {std::?stream<byte_t>} but the llvm libc++ seems to have
    //      trouble building streams over {unsigned char}
    // LAST CHECKED: 20220502 with llvm-13:
    //      implicit instantiation of undefined template std::codecvt<unsigned char, ...>
    using fstream_t = std::fstream;
    using ifstream_t = std::ifstream;
    using ofstream_t = std::ofstream;

} // namespace pyre::viz


// filters
namespace pyre::viz::filters {
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
} // namespace pyre::viz::filters

// conversions from other color spaces to {rgb}
namespace pyre::viz::colorspaces {
    inline auto hl(double h, double l, double threshold = 0.4) -> viz::rgb_t;
    inline auto hsb(double h, double s, double b) -> viz::rgb_t;
    inline auto hsl(double h, double s, double l) -> viz::rgb_t;
} // namespace pyre::viz::colorspaces

// color maps
namespace pyre::viz::colormaps {
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
} // namespace pyre::viz::colormaps


#endif

// end of file
