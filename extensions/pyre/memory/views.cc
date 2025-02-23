// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved


// the module initializers
#include "__init__.h"
// my views
#include "views.h"


// wrappers over {pyre::memory::view} template expansions
// build the submodule
void
pyre::py::memory::views::__init__(py::module & memory)
{
    // create a submodule for the view stores
    auto views = memory.def_submodule(
        // the name
        "views",
        // its docstring
        "view to storage owned by another entity");

    // get the pile of view types
    using views_t = pyre::memory::views_t;
    // build the classes
    expand(views, views_t {});

    // all done
    return;
}


// end of file
