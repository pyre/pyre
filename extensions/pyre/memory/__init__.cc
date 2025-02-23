// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved


// my package declarations
#include "__init__.h"


// the submodule
auto
pyre::py::memory::__init__(py::module & m) -> void
{
    // create a {memory} submodule
    auto memory = m.def_submodule(
        // the name of the module
        "memory",
        // its docstring
        "wrappers over {pyre::memory} template expansions");

    // cells
    cells::__init__(memory);
    // storage strategies


    // buffers on the heap
    heaps::__init__(memory);
    // file backed memory
    maps::__init__(memory);
    // borrowed memory
    views::__init__(memory);

    // all done
    return;
}


// end of file
