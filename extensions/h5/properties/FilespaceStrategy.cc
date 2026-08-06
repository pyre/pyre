// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// how a file manages the space its deleted objects leave behind
void
pyre::h5::py::properties::filespaceStrategy(py::module & m)
{
    // add bindings for the record
    auto cls = py::class_<FilespaceStrategy>(
        // in scope
        m,
        // class name
        "FilespaceStrategy",
        // docstring
        "how a file manages the space its deleted objects leave behind");

    // constructor; every field is named, so a call site says what its values mean
    cls.def(
        // the implementation
        py::init<H5F_fspace_strategy_t, bool, hsize_t>(),
        // the signature
        "strategy"_a, "persist"_a, "threshold"_a,
        // the docstring
        "describe how a file manages the space its deleted objects leave behind");

    // how free space is tracked
    cls.def_readwrite(
        // the name
        "strategy",
        // the field
        &FilespaceStrategy::strategy,
        // the docstring
        "how free space is tracked");

    // whether the free space survives closing the file
    cls.def_readwrite(
        // the name
        "persist",
        // the field
        &FilespaceStrategy::persist,
        // the docstring
        "whether the free space survives closing the file");

    // the smallest block worth tracking
    cls.def_readwrite(
        // the name
        "threshold",
        // the field
        &FilespaceStrategy::threshold,
        // the docstring
        "the smallest block worth tracking");

    // all done
    return;
}


// end of file
