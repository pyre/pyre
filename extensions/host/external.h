// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the platform configuration
#include <portinfo>
// on {macos} the cpu information comes from the kernel via {sysctl}
#if defined(HAVE_SYSCTL)
#include <sys/sysctl.h>
#endif
// STL
#include <cstddef>
#include <string>
// pybind11
#include <pybind11/pybind11.h>


// the aliases that shape this namespace
namespace pyre::extensions::host {
    // import {pybind11}
    namespace py = pybind11;
    // get the special {pybind11} literals, so that argument names can be spelled "name"_a
    using namespace py::literals;
} // namespace pyre::extensions::host


// end of file
