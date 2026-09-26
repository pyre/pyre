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


// make the cells within reach of the host
auto
pyre::py::grid::HostEngine::access() -> void
{
    // host cells are always within reach
    return;
}


// end of file
