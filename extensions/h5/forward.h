// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the {h5} extension namespace
namespace pyre::h5::py {
    // the module api
    void api(py::module &);

    // wrappers for the C++ HDF5 api
    // support
    void enums(py::module &);
    // attributes
    void attribute(py::module &);
    // datasets
    void dataspace(py::module &);
    void chunk(py::module &);
    void dataset(py::module &);
    // structural
    void group(py::module &);
    void file(py::module &);
    // the module-local flavors of the type-erased grid and mosaic
    void mosaics(py::module &);
} // namespace pyre::h5::py


// get the helpers
#include "attributes.h"
#include "data.h"


// end of file
