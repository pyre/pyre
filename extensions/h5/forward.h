// -*- c++ -*-
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

    // register the classes of the attributes
    void attributeClass(py::module &);
    // of the datasets
    void dataspaceClass(py::module &);
    void chunkClass(py::module &);
    void datasetClass(py::module &);
    // of the structural entities
    void groupClass(py::module &);
    void pageBufferStatsClass(py::module &);
    void fileClass(py::module &);
    // and the module-local flavors of the type-erased grid and mosaic
    void mosaicClasses(py::module &);

    // bind the attributes
    void attribute();
    // the datasets
    void dataspace(py::module &);
    void chunk();
    void dataset();
    // the structural entities
    void group();
    void pageBufferStats();
    void file();
    // the module-local flavors of the type-erased grid and mosaic
    void mosaics();
} // namespace pyre::h5::py


// get the helpers
#include "attributes.h"
#include "data.h"


// end of file
