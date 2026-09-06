// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// externals
#include "externals.h"


// set up the namespace
namespace pyre::py::memory {
    // the struct module code that describes a cell type to the python buffer protocol, with the
    // byte order marker a foreign order cell needs
    template <typename cellT>
    inline auto format() -> string_t;
} // namespace pyre::py::memory


// end of file
