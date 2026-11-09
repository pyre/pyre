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
    // register every class before binding any interface, since the signatures name the
    // classes they traffic in: the protocols
    nodeClasses(flow);
    // the descriptions of slots and settings
    descriptionClasses(flow);
    // the catalog
    catalogClasses(flow);
    // the tiles
    tileClasses(flow);
    // the variables
    variableClasses(flow);
    // and the rasters
    rasterClasses(flow);

    // now bind their interfaces: the protocols
    nodes();
    // the descriptions of slots and settings
    descriptions();
    // the catalog
    catalog(flow);
    // the tiles
    tiles();
    // the variables
    variables();
    // the rasters
    rasters(flow);
    // and the factories
    factories(flow);
    // all done
    return;
}


// end of file
