// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// external dependencies, and the aliases that shape this namespace
#include "external.h"


// the {libgsl} extension namespace
namespace gsl::py {
    // what the package says about itself
    void metadata(py::module & m);

    // the data types gsl allocates and releases
    void vector(py::module & m);
} // namespace gsl::py


// end of file
