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
    template <class sourceT>
    using amplitude_t = Amplitude<sourceT>;

    using constant_t = Constant;

    template <class sourceT>
    using phase_t = Phase<sourceT>;
} // namespace pyre::viz::filters

// conversions from other color spaces to {rgb}
namespace pyre::viz::colorspaces {
    auto hsb(double h, double s, double b) -> rgb_t;
    auto hsl(double h, double s, double l) -> rgb_t;
} // namespace pyre::viz::colorspaces

// color maps
namespace pyre::viz::colormaps {
    template <class sourceT>
    using complex_t = Complex<sourceT>;
}


#endif

// end of file
