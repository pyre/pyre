// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// the file format versions hdf5 may use
void
pyre::h5::py::properties::versionBounds(py::module & m)
{
    // add bindings for the record
    auto cls = py::class_<VersionBounds>(
        // in scope
        m,
        // class name
        "VersionBounds",
        // docstring
        "the file format versions hdf5 may use");

    // constructor; every field is named, so a call site says what its values mean
    cls.def(
        // the implementation
        py::init<H5F_libver_t, H5F_libver_t>(),
        // the signature
        "low"_a, "high"_a,
        // the docstring
        "describe the file format versions hdf5 may use");

    // the oldest format i may write
    cls.def_readwrite(
        // the name
        "low",
        // the field
        &VersionBounds::low,
        // the docstring
        "the oldest format i may write");

    // the newest format i may write
    cls.def_readwrite(
        // the name
        "high",
        // the field
        &VersionBounds::high,
        // the docstring
        "the newest format i may write");

    // all done
    return;
}


// end of file
