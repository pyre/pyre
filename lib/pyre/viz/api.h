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
    // extract the amplitude of a complex dataset
    template <class sourceT>
    using amplitude_t = Amplitude<sourceT>;
    // supply a constant value
    using constant_t = Constant;
    // scale values relative to a given interval
    template <class sourceT>
    using parametric_t = Parametric<sourceT>;
    // extract the phase of a complex dataset
    template <class sourceT>
    using phase_t = Phase<sourceT>;
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
