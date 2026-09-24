// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the python-support namespace
namespace pyre::py {
    // the classes here hold pybind11 objects, and pybind11 declares its whole namespace with
    // hidden visibility so that each extension module keeps its own copy of everything it
    // instantiates; a class of default visibility with hidden members draws a warning from
    // gcc, and would be wrong besides: every module registers these classes as module local
    // and never shares them across shared objects, so they are hidden the same way
    namespace grid __attribute__((visibility("hidden"))) {
        // the single type-erased grid the bindings hand to python, whatever the rank, cell
        // type, or storage strategy of the c++ grid it came from
        class AnyGrid;
        // its out-of-core sibling: the type-erased mosaic, whose cells python reaches tile
        // by tile through zero-copy panes
        class AnyMosaic;
    } // namespace grid
} // namespace pyre::py


// end of file
