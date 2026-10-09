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
    // bind the tiles over cells of type {cellT}, and register them with the catalog
    template <typename cellT>
    inline void bindTile(py::module & m)
    {
        // the tile
        using tile_type = tile_t<cellT>;
        // register it with the catalog
        registry().registerProduct<tile_type>();
        // its readable name, which must outlive the binding of the class
        auto name = tile_type::className();
        // bind it, under its readable name
        auto cls = py::classh<tile_type, product_t>(
            // the scope
            m,
            // the name of the class
            name.c_str(),
            // the docstring
            "a tile of cells");
        // its shape
        cls.def_property_readonly(
            // the name
            "shape",
            // the implementation
            [](const tile_type & self) -> std::tuple<int, int> {
                // get the shape
                auto shape = self.shape();
                // and hand off its extents
                return { shape[0], shape[1] };
            },
            // the docstring
            "my shape");
        // read access
        cls.def(
            // the name
            "read",
            // the implementation
            [](tile_type & self) -> anygrid_t {
                // pull my cells, refreshing them if they are stale, and hand off a view of them
                // that python may not write through
                return pyre::py::grid::anyGrid(self.read(), "heap").readonly();
            },
            // the docstring
            "refresh my cells if they are stale, and hand off a read-only view of them");
        // write access
        cls.def(
            // the name
            "write",
            // the implementation
            [](tile_type & self) -> anygrid_t {
                // get my cells
                auto & grid = self.write();
                // whatever reads them is about to be out of date; tell it now, since nothing
                // will know when the writing is over
                self.flush();
                // hand off a view of them that python may write through
                return pyre::py::grid::anyGrid(grid, "heap");
            },
            // the docstring
            "hand off a view of my cells that python may write through, and mark what depends "
            "on them as stale; write through it before the next pull");
        // all done
        return;
    }
} // namespace pyre::py::flow


// the tiles
void
pyre::py::flow::tiles(py::module & m)
{
    // real cells
    bindTile<pyre::memory::float32_t>(m);
    bindTile<pyre::memory::float64_t>(m);
    // complex cells
    bindTile<pyre::memory::complex64_t>(m);
    bindTile<pyre::memory::complex128_t>(m);
    // all done
    return;
}


// end of file
