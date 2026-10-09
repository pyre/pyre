// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// the factories of {pyre::viz} this extension was compiled with; python reaches them through
// the {Factory} protocol, so they go in the catalog rather than get classes of their own
void
pyre::py::viz::factories(py::module &)
{
    // the tiles
    using float32_t = pyre::py::flow::tile_t<pyre::memory::float32_t>;

    // get the catalog
    auto & catalog = pyre::py::flow::registry();
    // colormaps
    catalog.registerFactory<pyre::viz::factories::colormaps::gray_t<float32_t>>();
    // codecs
    catalog.registerFactory<pyre::viz::factories::codecs::bmp_t<float32_t>>();

    // all done
    return;
}


// end of file
