// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// dataset access property lists
void
pyre::h5::py::properties::dapl(py::module & m)
{
    // add bindings for hdf5 dataset access property lists
    auto cls = py::class_<DAPL, PropList>(
        // in scope
        m,
        // class name
        "dapl",
        // docstring
        "a dataset access property list");

    // static properties
    cls.def_property_readonly_static(
        // the name
        "default",
        // the implementation
        [](const py::object &) -> const DAPL & {
            // easy enough
            return DAPL::theDefault();
        },
        // we hand back a reference to a shared, library-owned object
        py::return_value_policy::reference,
        // docstring
        "the default dataset access property list");

    // constructor
    cls.def(
        // the implementation
        py::init(),
        // the docstring
        "build a dataset access property list");

    // interface
    // the chunk cache parameters
    cls.def_property(
        // the name
        "chunkCache",
        // the getter
        py::overload_cast<>(&DAPL::chunkCache, py::const_),
        // the setter
        py::overload_cast<const ChunkCache &>(&DAPL::chunkCache),
        // the docstring
        "the cache my datasets are read and written through");


    // all done
    return;
}


// end of file
