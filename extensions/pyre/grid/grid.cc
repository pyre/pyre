// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// wrappers over {pyre::grid::map} template expansions
// build the submodule
void
pyre::py::grid::grid(py::module & m)
{
    // create a {grid} submodule
    auto grid = m.def_submodule(
        // the name of the module
        "grid",
        // its docstring
        "wrappers over the various entities in {pyre::grid}");

    // indices
    indices(grid);
    // orders
    orders(grid);
    // shapes
    shapes(grid);
    // packings
    packings(grid);
    // grids
    grids(grid);

    // all done
    return;
}


// end of file
