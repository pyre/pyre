// -*- C++ -*-
// -*- coding: utf-8 -*-
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
            // the library prints its error stack on stderr every time it refuses a call; the
            // wrappers report refusals through journal, with the library's explanation, so the
            // print is noise nobody can silence. turn it off, so journal is the one voice
            if (H5Eset_auto2(H5E_DEFAULT, nullptr, nullptr) < 0) {
                // a refusal here is a bug in the runtime setup
                auto channel = pyre::journal::firewall_t("pyre.h5.init");
                // so complain
                channel << pyre::journal::at() << "failed to silence the hdf5 error stack"
                        << pyre::journal::endl;
            }
            // all done
            return;
        },
        // the docstring
        "initialize the hdf5 runtime: refusals are reported through journal, not on stderr");

    // the library's explanation of its latest refusal
    m.def(
        // the name
        "explanation",
        // the handler
        []() -> std::string {
            // ask the wrappers
            return pyre::h5::explanation();
        },
        // the docstring
        "the library's explanation of its latest refusal, or an empty string when it has none");

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

    // check whether a handle is alive
    m.def(
        // the name
        "valid",
        // the handler
        [](hid_t hid) -> bool {
            // ask the library
            return H5Iis_valid(hid) > 0;
        },
        // the signature
        "hid"_a,
        // the docstring
        "check whether {hid} refers to a live hdf5 object");

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
