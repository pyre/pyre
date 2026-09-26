// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// forward declarations
#include "forward.h"
// the engine of managed storage
#include "engine.h"
// the grids over cuda storage
#include <pyre/cuda/grid.h>
// the type-erased grid, the binding of its class, and the choice of cell type
#include <pyre/py/grid/AnyGrid.h>
#include <pyre/py/grid/bindings.h>
#include <pyre/py/grid/dispatch.h>


// the construction of grids on managed memory
namespace {
    // the type-erased grid
    using AnyGrid = pyre::py::grid::AnyGrid;
    // its signed integer type
    using size_type = AnyGrid::size_type;
    // the runtime-rank packing
    using packing_t = pyre::grid::dynamic_canonical_t;
    // its shape
    using shape_t = packing_t::shape_type;

    // a grid of {shape} cells of type {cellT} on fresh managed memory
    template <class cellT>
    auto makeManaged(const shape_t & shape) -> AnyGrid
    {
        // the grid
        using grid_t = pyre::cuda::grid::managed_t<packing_t, cellT>;
        // lay out the shape
        auto packing = packing_t(shape);
        // make the grid over enough cells on managed memory and type-erase it; managed storage
        // owns its cells
        return pyre::py::grid::anyGrid(grid_t { packing, packing.cells() }, "managed");
    }
} // namespace


// the grids on managed memory
auto
pyre::cuda::py::grids(py::module & m) -> void
{
    // the grid class, registered for this module alone
    pyre::py::grid::bindGrid<DeviceEngine>(
        // in the module
        m,
        // named
        "Grid",
        // the docstring
        "a multi-dimensional array whose cells live in cuda managed memory; its in-place "
        "arithmetic runs on the device, and the host waits for the device before it reaches the "
        "cells",
        // registered for this module alone
        true);

    // the factory
    m.def(
        // the name
        "managed",
        // the implementation
        [](const std::vector<size_type> & extents, const string_t & cell) -> AnyGrid {
            // adopt the extents as a shape
            const auto shape = shape_t(extents.begin(), extents.end());
            // pick the cell type and make the grid
            return pyre::py::grid::dispatchCell(
                cell, [&]<class cellT>() { return makeManaged<cellT>(shape); });
        },
        // the signature
        "shape"_a, "cell"_a,
        // the docstring
        "a grid of {shape} cells of type {cell} on fresh cuda managed memory");

    // all done
    return;
}


// end of file
