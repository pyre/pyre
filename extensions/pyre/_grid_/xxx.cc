// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved


// declarations
#include "xxx.h"


// wrappers over the {pyre::gird::index_t} expansions
auto
pyre::py::_grid_::xxx::__init__(py::module & grid) -> void
{
    // create a submodule for the xxx
    auto xxx = grid.def_submodule(
        // the name
        "xxx",
        // its docstring
        "[ replace with the xxx docstring]");

    // ge the pile of index expansions
    using xxx_t = pyre::typelists::types_t<>;
    // build the classes
    expand(xxx, xxx_t {});

    // all done
    return;
}

// end of file
