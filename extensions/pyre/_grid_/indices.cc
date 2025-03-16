// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved


// declarations
#include "indices.h"


// wrappers over the {pyre::gird::index_t} expansions
auto
pyre::py::_grid_::indices::__init__(py::module & grid) -> void
{
    // create a submodule for the indices
    auto indices = grid.def_submodule(
        // the name
        "indices",
        // its docstring
        "multi-dimensional indices");

    // ge the pile of index expansions
    using indices_t = pyre::grid::indices_t;
    // build the classes
    expand(indices, indices_t {});

    // all done
    return;
}

// end of file
