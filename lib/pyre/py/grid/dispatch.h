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


// the choice of a native cell type from its name, shared by every extension that makes grids
namespace pyre::py::grid {
    // call {f} with the native type of the cell named {cell}; {requested} is the name the
    // caller used, for the complaint when there is no such cell type
    template <class functionT>
    auto dispatchBase(const string_t & cell, const string_t & requested, functionT && f);

    // call {f} with the type of the cell named {cell}, honoring a trailing byte order marker:
    // {float64be} is a big endian double, {uint16le} a little endian unsigned short
    template <class functionT>
    auto dispatchCell(const string_t & cell, functionT && f);
} // namespace pyre::py::grid


// the inline implementations
#include "dispatch.icc"


// end of file
