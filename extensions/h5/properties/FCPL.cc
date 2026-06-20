// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// file creation property lists
void
pyre::h5::py::properties::fcpl(py::module & m)
{
    // add bindings for hdf5 file creation property lists
    auto cls = py::class_<FCPL, PropList>(
        // in scope
        m,
        // class name
        "fcpl",
        // docstring
        "a file creation property list");

    // static properties
    cls.def_property_readonly_static(
        // the name
        "default",
        // the implementation
        [](const py::object &) -> const FCPL & {
            // easy enough
            return FCPL::theDefault();
        },
        // we hand back a reference to a shared, library-owned object
        py::return_value_policy::reference,
        // docstring
        "the default file creation property list");

    // constructor
    cls.def(
        // the implementation
        py::init(),
        // the docstring
        "build a file creation property list");

    // interface
    // get the page size
    cls.def(
        // the name
        "getPageSize",
        // the implementation
        &FCPL::pageSize,
        // the docstring
        "retrieve the file space page size");

    // set the page size
    cls.def(
        // the name
        "setPageSize",
        // the implementation
        &FCPL::setPageSize,
        // the signature
        "size"_a,
        // the docstring
        "set the file space page {size}");

    // get the file space strategy
    cls.def(
        // the name
        "getFilespaceStrategy",
        // the implementation
        &FCPL::filespaceStrategy,
        // the docstring
        "get the current file space strategy");

    // set the file space strategy
    cls.def(
        // the name
        "setFilespaceStrategy",
        // the implementation
        &FCPL::setFilespaceStrategy,
        // the signature
        "strategy"_a, "persist"_a, "threshold"_a,
        // the docstring
        "set the file space strategy");

    // all done
    return;
}


// end of file
