// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// externals
#include "external.h"
// forward declarations
#include "forward.h"


// the cuda bindings
namespace pyre::py::cuda {
    // build the {cuda} submodule and its {cublas}/{cusolver}/{curand} children
    auto __init__(py::module &) -> void;
} // namespace pyre::py::cuda


// the individual libraries, named after nvidia's own so a caller who knows cublas/cusolver/
// curand already knows where to look
namespace pyre::py::cuda::cublas {
    auto __init__(py::module &) -> void;
} // namespace pyre::py::cuda::cublas

namespace pyre::py::cuda::cusolver {
    auto __init__(py::module &) -> void;
} // namespace pyre::py::cuda::cusolver

namespace pyre::py::cuda::curand {
    auto __init__(py::module &) -> void;
} // namespace pyre::py::cuda::curand


// end of file
