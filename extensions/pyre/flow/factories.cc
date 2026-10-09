// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// the factories of {pyre::flow} this extension was compiled with; python reaches them through
// the {Factory} protocol, so they go in the catalog rather than get classes of their own
void
pyre::py::flow::factories(py::module &)
{
    // the tiles
    using complex64_t = tile_t<pyre::memory::complex64_t>;
    using float64_t = tile_t<pyre::memory::float64_t>;
    using float32_t = tile_t<pyre::memory::float32_t>;

    // get the catalog
    auto & catalog = registry();
    // selectors
    catalog
        .registerFactory<pyre::flow::factories::selectors::amplitude_t<complex64_t, float64_t>>();
    // filters
    catalog.registerFactory<pyre::flow::factories::filters::parametric_t<float64_t, float32_t>>();
    // sources: a window of a raster, copied into a tile of the same cells
    catalog.registerFactory<
        pyre::flow::factories::sources::slice_t<raster_t<pyre::memory::float32_t>, float32_t>>();
    catalog.registerFactory<
        pyre::flow::factories::sources::slice_t<raster_t<pyre::memory::float64_t>, float64_t>>();
    catalog.registerFactory<pyre::flow::factories::sources::slice_t<
        raster_t<pyre::memory::complex64_t>, complex64_t>>();
    catalog.registerFactory<pyre::flow::factories::sources::slice_t<
        raster_t<pyre::memory::complex128_t>, tile_t<pyre::memory::complex128_t>>>();

    // all done
    return;
}


// end of file
