// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved


// module initializers
#include "__init__.h"
// the cell expansions
#include "cells.h"


// the cells module initializer
auto
pyre::py::memory::cells::__init__(py::module & memory) -> void
{
    // create a submodule for the cell types
    auto cells = memory.def_submodule(
        // the name of the module
        "cells",
        // its docstring
        "the cell type definitions");

    // get the pile of cell types
    using cells_t = pyre::memory::cells_t;
    // build the classes
    expand(cells, cells_t {});

    // all done
    return;
}


// end of file
