// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// the version number
#define HOST_VERSION "1.0"


// what the module says about itself
void
pyre::extensions::host::metadata(py::module & m)
{
    // the copyright note
    m.def(
        // the name
        "copyright",
        // the implementation
        []() -> std::string { return "host: (c) 1998-2026 Michael A.G. Aïvázis"; },
        // the docstring
        "the module copyright string");

    // the version
    m.def(
        // the name
        "version",
        // the implementation
        []() -> std::string { return HOST_VERSION; },
        // the docstring
        "the module version string");

    // all done
    return;
}


// end of file
