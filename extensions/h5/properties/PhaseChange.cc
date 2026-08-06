// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// the thresholds at which storage switches representation
void
pyre::h5::py::properties::phaseChange(py::module & m)
{
    // add bindings for the record
    auto cls = py::class_<PhaseChange>(
        // in scope
        m,
        // class name
        "PhaseChange",
        // docstring
        "the thresholds at which storage switches representation");

    // constructor; every field is named, so a call site says what its values mean
    cls.def(
        // the implementation
        py::init<unsigned int, unsigned int>(),
        // the signature
        "maxCompact"_a, "minDense"_a,
        // the docstring
        "describe the thresholds at which storage switches representation");

    // the count above which storage becomes indexed
    cls.def_readwrite(
        // the name
        "maxCompact",
        // the field
        &PhaseChange::maxCompact,
        // the docstring
        "the count above which storage becomes indexed");

    // the count below which it goes back to being inline
    cls.def_readwrite(
        // the name
        "minDense",
        // the field
        &PhaseChange::minDense,
        // the docstring
        "the count below which it goes back to being inline");

    // all done
    return;
}


// end of file
