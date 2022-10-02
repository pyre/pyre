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
pyre::h5::py::fapls::ros3(py::module & m)
{
#if defined(H5_HAVE_ROS3_VFD)
    // add bindings for the ros3 fapl
    auto fapl = py::class_<H5FD_ros3_fapl_t>(
        // in scope
        m,
        // class name
        "ROS3",
        // docstring
        "the ROS3 driver fapl");

    // constructor
    fapl.def(
        // the implementation
        py::init([](std::string region, std::string id, std::string key) {
            // make one
            H5FD_ros3_fapl_t p;
            // all done
            return p;
        }),
        // the signature
        "region"_a = "us-east-1", "id"_a = "", "key"_a = "",
        // the docstring
        "create a ROS3 parameter list");
#endif

    // all done
    return;
}


// end of file
