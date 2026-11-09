// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// home of all declarations that must be present in every translation unit
// e.g., the opaque data declarations
// subpackages that require access must include this file explicitly in their {__init__.h}


namespace pyre::h5::py::types {
    // make the module and register its classes
    void classes(py::module &);
    // the module initializer, which binds the interfaces of the registered classes
    void __init__(py::module &);
} // namespace pyre::h5::py::types


// end of file
