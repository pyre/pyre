// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved


// the module initializers
#include "__init__.h"
// my maps
#include "maps.h"


// wrappers over {pyre::memory::map_t} template expansions
void
pyre::py::memory::maps::__init__(py::module & memory)
{
    // create a submodule for the map stores
    auto maps = memory.def_submodule(
        // the name
        "maps",
        // its docstring
        "file backed storage");

    // get the pile of map types
    using maps_t = pyre::memory::maps_t;
    // build the classes
    expand(maps, maps_t {});

    // all done
    return;
}


// end of file
