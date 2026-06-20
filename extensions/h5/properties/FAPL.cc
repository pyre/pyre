// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// file access property lists
void
pyre::h5::py::properties::fapl(py::module & m)
{
    // add bindings for hdf5 file access property lists
    auto cls = py::class_<FAPL, PropList>(
        // in scope
        m,
        // class name
        "fapl",
        // docstring
        "a file access property list");

    // static properties
    cls.def_property_readonly_static(
        // the name
        "default",
        // the implementation
        [](const py::object &) -> const FAPL & {
            // easy enough
            return FAPL::theDefault();
        },
        // we hand back a reference to a shared, library-owned object
        py::return_value_policy::reference,
        // docstring
        "the default file access property list");

    // constructor
    cls.def(
        // the implementation
        py::init(),
        // the docstring
        "create a file access property list");

    // get the metadata block size
    cls.def(
        // the name
        "getMetaBlockSize",
        // the implementation
        &FAPL::metaBlockSize,
        // the docstring
        "retrieve the metadata block size");

    // set the metadata block size
    cls.def(
        // the name
        "setMetaBlockSize",
        // the implementation
        &FAPL::setMetaBlockSize,
        // the signature
        "size"_a,
        // the docstring
        "set the metadata cache parameters");

    // get the page buffer characteristics
    cls.def(
        // the name
        "getPageBufferSize",
        // the implementation
        &FAPL::pageBufferSize,
        // the docstring
        "retrieve the page buffer characteristics");

    // set the page buffer characteristics
    cls.def(
        // the name
        "setPageBufferSize",
        // the implementation
        &FAPL::setPageBufferSize,
        // the signature
        "page"_a, "meta"_a = 0, "raw"_a = 0,
        // the docstring
        "set the page buffer characteristics");


#if defined(H5_HAVE_ROS3_VFD)
    // populate the property list with ros3 parameters
    cls.def(
        // the name
        "ros3",
        // the implementation
        &FAPL::ros3,
        // the signature
        "authenticate"_a = true, "region"_a = "", "id"_a = "", "key"_a = "", "token"_a = "",
        // we hand back a reference to the list we just configured
        py::return_value_policy::reference,
        // the docstring
        "populate the property list with ros3 parameters");
#endif

    // all done
    return;
}


// end of file
