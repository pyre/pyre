// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// forward declarations
#include "forward.h"
// my declarations
#include "__init__.h"


// build the {cuda} submodule
auto
pyre::py::cuda::__init__(py::module & m) -> void
{
    // make the submodule
    auto cuda = m.def_submodule(
        // the name
        "cuda",
        // the docstring
        "thin bindings for cublas, cusolver, and curand, over pyre's own grids");

    // the individual libraries, each named after nvidia's own, and each thin: one function per
    // routine, an explicit handle on every call, and grids in place of raw device pointers
    cublas::__init__(cuda);
    cusolver::__init__(cuda);
    curand::__init__(cuda);
}


// end of file
