// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"
// my declarations
#include "__init__.h"


// the package initializer
void
pyre::py::flow::__init__(py::module & m)
{
    // create a {flow} submodule
    auto flow = m.def_submodule(
        // the name of the module
        "flow",
        // its docstring
        "wrappers over {pyre::flow} entities");
    // the protocols
    nodes(flow);
    // the descriptions of slots and settings
    descriptions(flow);
    // the catalog
    catalog(flow);
    // the tiles
    tiles(flow);
    // and the factories
    factories(flow);
    // all done
    return;
}


// end of file
