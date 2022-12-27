// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// wrappers over {pyre::memory::map} template expansions
// build the submodule
void
pyre::py::memory::memory(py::module & m)
{
    // create a {memory} submodule
    auto memory = m.def_submodule(
        // the name of the module
        "memory",
        // its docstring
        "wrappers over {pyre::memory::map_t} template expansions");

    // add the various maps
    maps(memory);

    // all done
    return;
}


// end of file
