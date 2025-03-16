// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved


// package declaration
#include "__init__.h"


// wrappers over {pyre::grid::map} template expansions
// build the submodule
auto
pyre::py::_grid_::__init__(py::module & m) -> void
{
    // create a {grid} submodule
    auto grid = m.def_submodule(
        // the name of the module
        "_grid_",
        // its docstring
        "wrappers over the various entities in {pyre::grid}");

    // indices
    indices::__init__(grid);

    // all done
    return;
}


// end of file
