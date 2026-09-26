// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// forward declarations
#include "forward.h"
// the engine of managed storage
#include "engine.h"


// the module functions
auto
pyre::cuda::py::api(py::module & m) -> void
{
    // wait for the device
    m.def(
        // the name
        "synchronize",
        // the implementation
        &DeviceEngine::access,
        // the docstring
        "wait for the device to finish the work queued on it");

    // all done
    return;
}


// end of file
