// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the pyre extension namespace for the grid bindings
namespace pyre::py::grid {
    // the single type-erased grid the bindings hand to python, whatever the rank, cell type, or
    // storage strategy of the c++ grid it came from
    class AnyGrid;
    // its out-of-core sibling: the type-erased mosaic, whose cells python reaches tile by tile
    // through zero-copy panes
    class AnyMosaic;
} // namespace pyre::py::grid


// end of file
