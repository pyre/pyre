// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// the widths hdf5 records positions and lengths in
void
pyre::h5::py::properties::sizes(py::module & m)
{
    // add bindings for the record
    auto cls = py::class_<Sizes>(
        // in scope
        m,
        // class name
        "Sizes",
        // docstring
        "the widths hdf5 records positions and lengths in");

    // constructor; every field is named, so a call site says what its values mean
    cls.def(
        // the implementation
        py::init<std::size_t, std::size_t>(),
        // the signature
        "offsets"_a, "lengths"_a,
        // the docstring
        "describe the widths hdf5 records positions and lengths in");

    // how many bytes a position in the file takes
    cls.def_readwrite(
        // the name
        "offsets",
        // the field
        &Sizes::offsets,
        // the docstring
        "how many bytes a position in the file takes");

    // how many bytes a length takes
    cls.def_readwrite(
        // the name
        "lengths",
        // the field
        &Sizes::lengths,
        // the docstring
        "how many bytes a length takes");

    // all done
    return;
}


// end of file
