// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// file objects
void
pyre::h5::py::fapl(py::module & m)
{
    // add bindings for hdf5 file objects
    auto cls = py::class_<FileAccessPropertyList>(
        // in scope
        m,
        // class name
        "FAPL",
        // docstring
        "a file access property list");

    // constructor
    cls.def(
        // the implementation
        py::init(),
        // the docstring
        "create a file access property list");

    // close the list
    cls.def(
        // the name
        "close",
        // the implementation
        &FileAccessPropertyList::close,
        // the docstring
        "discard the property list");

#if defined(H5_HAVE_ROS3_VFD)
    // populate the property list with ros3 parameters
    cls.def(
        // the name
        "ros3",
        // the implementation
        [](FileAccessPropertyList & plist) -> FileAccessPropertyList & {
            // all done
            return plist;
        },
        // the signature
        // the docstring
        "populate the property list with ros3 parameters");
#endif

    // all done
    return;
}


// end of file
