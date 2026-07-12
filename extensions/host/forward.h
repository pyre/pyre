// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// external dependencies, and the aliases that shape this namespace
#include "external.h"


// the {host} extension namespace
namespace pyre::extensions::host {
    // what the module says about itself
    void metadata(py::module & m);
    // the cpu resource counts this host reports
    void cpu(py::module & m);
} // namespace pyre::extensions::host


// end of file
