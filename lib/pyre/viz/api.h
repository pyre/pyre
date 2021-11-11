// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2021 all rights reserved

// code guard
#if !defined(pyre_viz_api_h)
#define pyre_viz_api_h


// publicly visible types
namespace pyre::viz {

    // codecs
    // microsoft bmp
    using bmp_t = BMP;

} // namespace pyre::viz


// filters
namespace pyre::viz::filters {
    // a filter that adds two others
    template <class op1T, class op2T>
    using add_t = Add<op1T, op2T>;
    // extract the amplitude of a complex dataset
    template <class sourceT>
    using amplitude_t = Amplitude<sourceT>;
    // supply a constant value
    template <typename valueT = double>
    using constant_t = Constant<valueT>;
    // a filter that maps values in [0,1] to the index of of a call in a geometrically spaced grid
    template <class sourceT>
    using geometric_t = Geometric<sourceT>;
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
    // a filter that maps values in [0,1] to the index of of a call in a uniformly spaced grid
    template <class sourceT>
    using uniform_t = Uniform<sourceT>;
} // namespace pyre::viz::filters

// conversions from other color spaces to {rgb}
namespace pyre::viz::colorspaces {
    auto hsb(double h, double s, double b) -> viz::rgb_t;
    auto hsl(double h, double s, double l) -> viz::rgb_t;
} // namespace pyre::viz::colorspaces

// color maps
namespace pyre::viz::colormaps {
    template <class sourceT>
    using complex_t = Complex<sourceT>;

    template <class sourceT>
    using gray_t = Gray<sourceT>;

    template <class hueSourceT, class saturationSourceT, class brightnessSourceT>
    using hsb_t = HSB<hueSourceT, saturationSourceT, brightnessSourceT>;

    template <class hueSourceT, class saturationSourceT, class luminositySourceT>
    using hsl_t = HSB<hueSourceT, saturationSourceT, luminositySourceT>;

    template <class redSourceT, class greenSourceT, class blueSourceT>
    using rgb_t = RGB<redSourceT, greenSourceT, blueSourceT>;
} // namespace pyre::viz::colormaps


#endif

// end of file
