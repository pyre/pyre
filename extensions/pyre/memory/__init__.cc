// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"
// my package declarations
#include "__init__.h"

// wrappers over {pyre::memory} template expansions
// build the submodule
void
pyre::py::memory::__init__(py::module & m)
{
    // create a {memory} submodule
    auto memory = m.def_submodule(
        // the name of the module
        "memory",
        // its docstring
        "wrappers over {pyre::memory} template expansions");

    // buffers on the heap
    heaps(memory);
    // file backed memory
    maps(memory);

    // all done
    return;
}


// end of file
