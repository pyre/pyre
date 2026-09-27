// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// externals
#include "externals.h"
// forward declarations
#include "forward.h"
// the type-erased grid
#include "AnyGrid.h"
// the translation of python operands for in-place arithmetic
#include "inplace.h"


// the binding of the grid class, shared by every extension that makes grids
namespace pyre::py::grid {
    // bind the grid class as {name} in {module}, registered for that module alone when {local}
    // is set; {engineT} knows how to reach the cells: its {access} runs before the host touches
    // them, so storage the host shares with a device can wait for the device first
    template <class engineT>
    auto bindGrid(py::module & module, const char * name, const char * docstring, bool local)
        -> py::class_<AnyGrid>;
} // namespace pyre::py::grid


// the inline implementations
#include "bindings.icc"


// end of file
