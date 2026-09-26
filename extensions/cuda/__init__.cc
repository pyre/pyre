// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"
// my package declarations
#include "__init__.h"


// the module entry point
PYBIND11_MODULE(cuda, m)
{
    // the docstring
    m.doc() = "the cuda extension module";
    // the module functions
    pyre::cuda::py::api(m);
    // the grids on managed memory
    pyre::cuda::py::grids(m);
    // all done
    return;
}


// end of file
