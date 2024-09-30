// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// add global bindings to the module
void
pyre::h5::py::api(py::module & m)
{
    // initialize the library
    m.def(
        // the name
        "init",
        // the handler
        []() -> void {
            // turn off the native diagnostics; we commit to catching all exceptions and
            // generating our own messages
            // H5::Exception::dontPrint();
            // all done
            return;
        },
        // the docstring
        "initialize the hdf5 runtime");

    // get the version
    m.def(
        // the name
        "version",
        // the handler
        []() {
            // get the version and return it
            return std::make_tuple(H5_VERS_MAJOR, H5_VERS_MINOR, H5_VERS_RELEASE);
        },
        // the docstring
        "initialize the hdf5 runtime");

    // check whether there is ROS3 support
    m.def(
        // the name
        "ros3",
        // the handler
        []() -> bool {
#if defined(H5_HAVE_ROS3_VFD)
            return true;
#else
            return false;
#endif
        },
        // the docstring
        "check whether there is ROS3 support");

    // all done
    return;
}


// end of file
