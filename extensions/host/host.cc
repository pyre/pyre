// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// the module entry point
PYBIND11_MODULE(host, m)
{
    // the doc string
    m.doc() = "provides access to host specific information";

    // module metadata
    pyre::extensions::host::metadata(m);
    // the cpu resource counts
    pyre::extensions::host::cpu(m);
}


// end of file
