// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// helpers
namespace pyre::py::flow {
    // register what the channels over complex cells of type {cellT} need: the slice of a raster
    // into tiles of the same cells, and the stages that turn complex values into reals in double
    // precision, the way the iterators compute them
    template <typename cellT>
    inline void complexChannels(catalog_t & catalog)
    {
        // the tiles
        using signal_t = tile_t<cellT>;
        using real_t = tile_t<pyre::memory::float64_t>;
        // the slice
        catalog
            .registerFactory<pyre::flow::factories::sources::slice_t<raster_t<cellT>, signal_t>>();
        // the parts of a complex value
        catalog.registerFactory<pyre::flow::factories::selectors::amplitude_t<signal_t, real_t>>();
        catalog.registerFactory<pyre::flow::factories::selectors::real_t<signal_t, real_t>>();
        catalog.registerFactory<pyre::flow::factories::selectors::imaginary_t<signal_t, real_t>>();
        // and its phase, placed in an interval
        catalog.registerFactory<pyre::flow::factories::filters::cycle_t<signal_t, real_t>>();
        // all done
        return;
    }

    // register what the channels over real cells of type {cellT} need: the slice of a raster
    // into tiles of doubles, so every cell type reaches the normalizer exactly
    template <typename cellT>
    inline void realChannels(catalog_t & catalog)
    {
        // the slice
        catalog.registerFactory<pyre::flow::factories::sources::slice_t<
            raster_t<cellT>, tile_t<pyre::memory::float64_t>>>();
        // all done
        return;
    }
} // namespace pyre::py::flow


// the factories of {pyre::flow} this extension was compiled with; python reaches them through
// the {Factory} protocol, so they go in the catalog rather than get classes of their own
void
pyre::py::flow::factories(py::module &)
{
    // the tiles of reals
    using float64_t = tile_t<pyre::memory::float64_t>;
    using float32_t = tile_t<pyre::memory::float32_t>;

    // get the catalog
    auto & catalog = registry();

    // channels over complex cells
    complexChannels<pyre::memory::complex64_t>(catalog);
    complexChannels<pyre::memory::complex128_t>(catalog);

    // channels over real cells
    // signed integers
    realChannels<pyre::memory::int8_t>(catalog);
    realChannels<pyre::memory::int16_t>(catalog);
    realChannels<pyre::memory::int32_t>(catalog);
    realChannels<pyre::memory::int64_t>(catalog);
    // unsigned integers
    realChannels<pyre::memory::uint8_t>(catalog);
    realChannels<pyre::memory::uint16_t>(catalog);
    realChannels<pyre::memory::uint32_t>(catalog);
    realChannels<pyre::memory::uint64_t>(catalog);
    // floating point
    realChannels<pyre::memory::float32_t>(catalog);
    realChannels<pyre::memory::float64_t>(catalog);

    // the stages every channel shares
    // the map of an interval onto [0,1], in single precision, the way the iterators make it
    catalog.registerFactory<pyre::flow::factories::filters::parametric_t<float64_t, float32_t>>();
    // and in double precision, for the values that become hues
    catalog.registerFactory<pyre::flow::factories::filters::parametric_t<float64_t, float64_t>>();
    // the power law, which turns amplitudes into brightnesses, painted gray in single precision
    catalog.registerFactory<pyre::flow::factories::filters::power_t<float64_t, float32_t>>();
    // and into luminosities in double precision
    catalog.registerFactory<pyre::flow::factories::filters::power_t<float64_t, float64_t>>();
    // the map of an interval onto another, which turns phases into hues
    catalog.registerFactory<pyre::flow::factories::filters::affine_t<float64_t, float64_t>>();
    // a constant, such as a saturation or a brightness
    catalog.registerFactory<pyre::flow::factories::filters::constant_t<float64_t>>();

    // all done
    return;
}


// end of file
