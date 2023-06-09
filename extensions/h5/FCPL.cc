// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// file creation property lists
void
pyre::h5::py::fcpl(py::module & m)
{
    // add bindings for hdf5 file creation property lists
    auto cls = py::class_<FCPL, PropList>(
        // in scope
        m,
        // class name
        "FCPL",
        // docstring
        "a file creation property list");

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
        &FCPL::getFileSpacePagesize,
        // the signature
        // the docstring
        "retrieve the file space page size");

    // set the page size
    cls.def(
        // the name
        "setPageSize",
        // the implementation
        &FCPL::setFileSpacePagesize,
        // the signature
        "size"_a,
        // the docstring
        "set the file space page {size}");

    // all done
    return;
}


// end of file
