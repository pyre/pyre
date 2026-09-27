// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the type-erased grid
#include <pyre/py/grid/AnyGrid.h>


// the support shared by the bindings of the cuda libraries
namespace pyre::cuda::py {
    // the library handle carried by the integer {handle}, the way python holds it
    template <class handleT>
    inline auto toHandle(std::uintptr_t handle) -> handleT;

    // the integer python carries for the library {handle}
    template <class handleT>
    inline auto fromHandle(handleT handle) -> std::uintptr_t;

    // the device address of the cells of {grid}, which must be of type {expected} and on storage
    // the device reaches; {routine} names the caller, for the complaints
    inline auto data(pyre::py::grid::AnyGrid & grid, char expected, const char * routine) -> void *;
} // namespace pyre::cuda::py


// the inline implementations
#include "support.icc"


// end of file
