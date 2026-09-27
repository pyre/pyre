// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the type-erased classes these bindings register live in the library's python-support
// tier; get their forward declarations from there
#include <pyre/py/grid/forward.h>


// the classes of these bindings
namespace pyre::py::grid {
    // the engine that reaches the cells of grids on host storage
    class HostEngine;
} // namespace pyre::py::grid


// end of file
