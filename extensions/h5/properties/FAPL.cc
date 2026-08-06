// -*- C++ -*-
// -*- coding: utf-8 -*-
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

    // interface
    // the metadata block size
    cls.def_property(
        // the name
        "metadataBlockSize",
        // the getter
        py::overload_cast<>(&FAPL::metadataBlockSize, py::const_),
        // the setter
        py::overload_cast<hsize_t>(&FAPL::metadataBlockSize),
        // the docstring
        "the size of the blocks my metadata is allocated in");

    // the page buffer characteristics
    cls.def_property(
        // the name
        "pageBufferSize",
        // the getter
        py::overload_cast<>(&FAPL::pageBufferSize, py::const_),
        // the setter
        py::overload_cast<const PageBuffer &>(&FAPL::pageBufferSize),
        // the docstring
        "my page buffer, as {(bytes, metadata percent, raw data percent)}");

    // the alignment of objects in the file
    cls.def_property(
        // the name
        "alignment",
        // the getter
        py::overload_cast<>(&FAPL::alignment, py::const_),
        // the setter
        py::overload_cast<const Alignment &>(&FAPL::alignment),
        // the docstring
        "where objects start in my file, as {(threshold, alignment)} bytes");

    // the sieve buffer
    cls.def_property(
        // the name
        "sieveBufferSize",
        // the getter
        py::overload_cast<>(&FAPL::sieveBufferSize, py::const_),
        // the setter
        py::overload_cast<std::size_t>(&FAPL::sieveBufferSize),
        // the docstring
        "the size of the buffer that gathers small writes to contiguous datasets");

    // the file close degree
    cls.def_property(
        // the name
        "closeDegree",
        // the getter
        py::overload_cast<>(&FAPL::closeDegree, py::const_),
        // the setter
        py::overload_cast<H5F_close_degree_t>(&FAPL::closeDegree),
        // the docstring
        "what becomes of my file when its handle closes with objects still open");

    // the default caches
    cls.def_property(
        // the name
        "cache",
        // the getter
        py::overload_cast<>(&FAPL::cache, py::const_),
        // the setter
        py::overload_cast<const Cache &>(&FAPL::cache),
        // the docstring
        "my default caches, as {(metadata elements, chunk slots, chunk bytes, preemption)}");

    // the file format version bounds
    cls.def_property(
        // the name
        "libverBounds",
        // the getter
        py::overload_cast<>(&FAPL::libverBounds, py::const_),
        // the setter
        py::overload_cast<const VersionBounds &>(&FAPL::libverBounds),
        // the docstring
        "the file format versions i may use, as {(low, high)}; asking for a recent one "
        "buys newer features and narrows who can read the result");

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
