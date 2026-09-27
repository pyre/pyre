// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the vocabulary of in-place arithmetic
#include <pyre/py/grid/arithmetic.h>


// the device code includes this header without the rest of the extension, so it declares its
// own namespace
namespace pyre::cuda::py {
    // the engine that reaches the cells of grids on managed storage
    class DeviceEngine;
} // namespace pyre::cuda::py


// the engine that reaches the cells of grids on managed storage: the device does the arithmetic,
// without waiting, and the host waits for the device before it touches the cells
class pyre::cuda::py::DeviceEngine {
    // types
public:
    // me
    using self_type = DeviceEngine;
    // the vocabulary of in-place arithmetic
    using operation_type = pyre::py::grid::arithmetic::Operation;
    using cell_type = pyre::py::grid::arithmetic::Cell;
    using layout_type = pyre::py::grid::arithmetic::Layout;
    using scalar_type = pyre::py::grid::arithmetic::Scalar;

    // interface
public:
    // make the cells within reach of the host, by waiting for the device
    static auto access() -> void;
    // whether the engine reaches cells in host memory; the device does not
    static constexpr bool reachesHost = false;
    // combine the cells of {source} into the cells of {target}, on the device
    static auto apply(
        operation_type op, cell_type cell, const layout_type & target, const layout_type & source)
        -> void;
    // combine {value} into the cells of {target}, on the device
    static auto apply(
        operation_type op, cell_type cell, const layout_type & target, const scalar_type & value)
        -> void;

    // metamethods
public:
    // an engine is a collection of static functions, so there are no instances
    DeviceEngine() = delete;
    // destructor
    ~DeviceEngine() = delete;
    // copy and move
    DeviceEngine(const DeviceEngine &) = delete;
    DeviceEngine(DeviceEngine &&) = delete;
    DeviceEngine & operator=(const DeviceEngine &) = delete;
    DeviceEngine & operator=(DeviceEngine &&) = delete;
};


// end of file
