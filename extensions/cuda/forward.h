// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the {cuda} extension namespace
namespace pyre::cuda::py {
    // the engine that reaches the cells of grids on managed storage
    class DeviceEngine;

    // the module functions
    void api(py::module &);
    // the grids on managed memory
    void grids(py::module &);
    // the cublas bindings
    void cublas(py::module &);
    // the cusolver bindings
    void cusolver(py::module &);
    // the curand bindings
    void curand(py::module &);
} // namespace pyre::cuda::py


// end of file
