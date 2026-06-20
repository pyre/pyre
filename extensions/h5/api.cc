// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


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
            // a hook for runtime initialization, e.g. silencing the native diagnostics in favor
            // of pyre journal messages, via {H5Eset_auto2}
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
