// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// register the class, so that every signature can name it
void
pyre::h5::py::properties::phaseChangeClass(py::module & m)
{
    // register the class of the record
    py::class_<PhaseChange>(
        // in scope
        m,
        // class name
        "PhaseChange",
        // docstring
        "the thresholds at which storage switches representation");

    // all done
    return;
}


// the thresholds at which storage switches representation
void
pyre::h5::py::properties::phaseChange()
{
    // the class, registered by {phaseChangeClass}
    auto cls = py::class_<PhaseChange>(py::type::of<PhaseChange>());

    // constructor; every field is named, so a call site says what its values mean
    cls.def(
        // the implementation
        py::init<unsigned int, unsigned int>(),
        // the signature
        "maxCompact"_a, "minDense"_a,
        // the docstring
        "describe the thresholds at which storage switches representation");

    // the count above which storage becomes indexed
    cls.def_property(
        // the name
        "maxCompact",
        // the getter
        pyre::py::getter(cls, &PhaseChange::maxCompact),
        // the setter
        pyre::py::setter(cls, &PhaseChange::maxCompact),
        // the docstring
        "the count above which storage becomes indexed");

    // the count below which it goes back to being inline
    cls.def_property(
        // the name
        "minDense",
        // the getter
        pyre::py::getter(cls, &PhaseChange::minDense),
        // the setter
        pyre::py::setter(cls, &PhaseChange::minDense),
        // the docstring
        "the count below which it goes back to being inline");

    // all done
    return;
}


// end of file
