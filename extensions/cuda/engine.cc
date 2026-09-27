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
#include "engine.h"


// make the cells within reach of the host, by waiting for the device
auto
pyre::cuda::py::DeviceEngine::access() -> void
{
    // wait for the device
    const auto status = cudaDeviceSynchronize();
    // if it reports a failure of the work it was doing
    if (status != cudaSuccess) {
        // raise it
        throw std::runtime_error(string_t("pyre.cuda: ") + cudaGetErrorString(status));
    }
    // all done
    return;
}


// end of file
