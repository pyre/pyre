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
pyre::h5::py::fapls::fapls(py::module & m)
{
    // make a new namespace to hold fapl descriptions
    auto fapls = m.def_submodule(
        // the name of the module
        "fapls",
        // its docstring
        "HDF5 file access parameter list types");

    // all done
    return;
}


// end of file
