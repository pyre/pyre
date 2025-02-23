// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved


// module initializers
#include "__init__.h"
// heaps
#include "heaps.h"


// wrappers over {pyre::memory::heap_t} template expansions
void
pyre::py::memory::heaps::__init__(py::module & memory)
{
    // create a submodule for the heap stores
    auto heaps = memory.def_submodule(
        // the name
        "heaps",
        // its docstring
        "storage on the heap");

    // get the pile of heap types
    using heaps_t = pyre::memory::heaps_t;
    // build the classes
    expand(heaps, heaps_t {});

    // all done
    return;
}


// end of file
