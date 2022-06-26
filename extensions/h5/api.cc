// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved


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
            H5::Exception::dontPrint();
            // all done
            return;
        },
        // the docstring
        "initialize the hdf5 runtime");

    // all done
    return;
}


// end of file
