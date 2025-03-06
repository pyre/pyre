// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved


// module initializers
#include "__init__.h"
// buffers
#include "buffers.h"


// wrappers over {pyre::memory::buffer_t} template expansions
void
pyre::py::memory::buffers::__init__(py::module & memory)
{
    // create a submodule for the buffer stores
    auto buffers = memory.def_submodule(
        // the name
        "buffers",
        // its docstring
        "storage on the buffer");

    // get the pile of buffer types
    using buffers_t = pyre::memory::buffers_t;
    // build the classes
    expand(buffers, buffers_t {});

    // all done
    return;
}


// end of file
