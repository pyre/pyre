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
    // apply {step} to each kind of cell there are tiles of
    template <class stepT>
    inline void tileCells(stepT step)
    {
        // real cells
        step.template operator()<pyre::memory::float32_t>();
        step.template operator()<pyre::memory::float64_t>();
        // complex cells
        step.template operator()<pyre::memory::complex64_t>();
        step.template operator()<pyre::memory::complex128_t>();
        // all done
        return;
    }

    // register the class of the tiles over cells of type {cellT}, so that every signature can
    // name it
    template <typename cellT>
    inline void tileClass(py::module & m)
    {
        // the tile
        using tile_type = tile_t<cellT>;
        // its readable name, which must outlive the registration of the class
        auto name = tile_type::className();
        // register it, under its readable name
        py::classh<tile_type, product_t>(
            // the scope
            m,
            // the name of the class
            name.c_str(),
            // the docstring
            "a tile of cells");
        // all done
        return;
    }

    // bind the tiles over cells of type {cellT}, and register them with the catalog
    template <typename cellT>
    inline void bindTile()
    {
        // the tile
        using tile_type = tile_t<cellT>;
        // register it with the catalog
        registry().registerProduct<tile_type>();
        // its class, registered by {tileClass}
        auto cls = py::classh<tile_type, product_t>(py::type::of<tile_type>());
        // the spelling of its type, which is its key in the catalog
        cls.def_property_readonly_static(
            // the name
            "decl",
            // the implementation
            [](const py::object &) -> string_t { return tile_type::declSelf(); },
            // the docstring
            "the declaration of my type, which is my key in the catalog");
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
                // get my cells, which marks whatever is computed from them as stale
                auto & grid = self.write();
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


// register the classes of the tiles, so that every signature can name them
void
pyre::py::flow::tileClasses(py::module & m)
{
    // one kind of cell at a time
    tileCells([&m]<typename cellT>() {
        // register the class of its tiles
        tileClass<cellT>(m);
        // all done
        return;
    });
    // all done
    return;
}


// the tiles
void
pyre::py::flow::tiles()
{
    // one kind of cell at a time
    tileCells([]<typename cellT>() {
        // bind its tiles
        bindTile<cellT>();
        // all done
        return;
    });
    // all done
    return;
}


// end of file
