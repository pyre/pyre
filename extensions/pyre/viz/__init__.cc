// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"
// package declarations
#include "__init__.h"


// wrappers over {pyre::viz} entities
// build the submodule
void
pyre::py::viz::__init__(py::module & m)
{
    // create a {viz} submodule
    auto viz = m.def_submodule(
        // the name of the module
        "viz",
        // its docstring
        "wrappers over {pyre::viz} entities");

    // add the bitmap bindings
    bmp(viz);

    // all done
    return;
}


// end of file
