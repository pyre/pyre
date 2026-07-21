// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// forward declarations
#include "forward.h"
// my declarations
#include "__init__.h"
// the erased grid and the {erase} converter
#include "Grid.h"


// the erased grid measures with a signed integer, matching the c++ library
using size_type = pyre::py::grid::Grid::size_type;
// the runtime-rank packing the factory builds, so that only the cell type needs dispatch
using packing_t = pyre::grid::dynamic_canonical_t;
// its shape carries one signed extent per axis
using shape_t = packing_t::shape_type;


// allocate a fresh heap grid of the given shape and cell type, and hand back the erased form
// the packing is runtime-rank, so this dispatches on the cell type alone: twelve leaf
// instantiations, not twelve times a span of ranks
namespace pyre::py::grid {
    // build a heap grid over {shape} with cells of type {cellT}
    template <class cellT>
    auto makeHeap(const shape_t & shape) -> Grid
    {
        // the storage strategy for this cell type
        using storage_t = pyre::memory::heap_t<cellT>;
        // and the grid that composes the runtime packing with it
        using grid_t = pyre::grid::grid_t<packing_t, storage_t>;
        // lay out the shape
        auto packing = packing_t(shape);
        // put enough cells on the heap to hold it
        auto storage = storage_t { packing.cells() };
        // make the grid and erase it, tagging its storage kind
        return erase(grid_t { packing, storage }, "heap");
    }

    // the factory python calls: choose the cell type from a numpy style dtype string
    auto heap(const std::vector<size_type> & extents, const string_t & dtype) -> Grid
    {
        // adopt the extents as a shape
        auto shape = shape_t(extents.begin(), extents.end());
        // signed integers
        if (dtype == "int8")
            return makeHeap<pyre::memory::int8_t>(shape);
        if (dtype == "int16")
            return makeHeap<pyre::memory::int16_t>(shape);
        if (dtype == "int32")
            return makeHeap<pyre::memory::int32_t>(shape);
        if (dtype == "int64")
            return makeHeap<pyre::memory::int64_t>(shape);
        // unsigned integers
        if (dtype == "uint8")
            return makeHeap<pyre::memory::uint8_t>(shape);
        if (dtype == "uint16")
            return makeHeap<pyre::memory::uint16_t>(shape);
        if (dtype == "uint32")
            return makeHeap<pyre::memory::uint32_t>(shape);
        if (dtype == "uint64")
            return makeHeap<pyre::memory::uint64_t>(shape);
        // floating point
        if (dtype == "float32")
            return makeHeap<pyre::memory::float32_t>(shape);
        if (dtype == "float64")
            return makeHeap<pyre::memory::float64_t>(shape);
        // complex
        if (dtype == "complex64")
            return makeHeap<pyre::memory::complex64_t>(shape);
        if (dtype == "complex128")
            return makeHeap<pyre::memory::complex128_t>(shape);

        // anything else is a caller mistake
        auto channel = pyre::journal::error_t("pyre.grid.bindings");
        // complain
        channel << "unsupported grid cell type '" << dtype << "'" << pyre::journal::endl(__HERE__);
        // and refuse
        throw py::value_error("unsupported grid cell type '" + dtype + "'");
    }
} // namespace pyre::py::grid


// build the {grid} submodule
auto
pyre::py::grid::__init__(py::module & m) -> void
{
    // make the submodule
    auto grid = m.def_submodule(
        // the name
        "grid",
        // the docstring
        "multi-dimensional arrays over pluggable memory");

    // the single erased grid class, presenting the python buffer protocol so numpy and friends
    // can view its cells with no copy
    auto cls = py::class_<Grid>(
        // in the submodule
        grid,
        // named
        "Grid",
        // exposing the buffer protocol
        py::buffer_protocol(),
        // the docstring
        "a multi-dimensional array whose cells live behind a storage strategy");

    // wire the buffer protocol to the erased grid's own description
    cls.def_buffer([](Grid & self) -> py::buffer_info { return self.view(); });

    // the extent along each axis
    cls.def_property_readonly(
        // the name
        "shape",
        // the getter
        &Grid::shape,
        // the docstring
        "my extent along each axis");

    // the strides, in cells
    cls.def_property_readonly(
        // the name
        "strides",
        // the getter
        &Grid::strides,
        // the docstring
        "the distance between consecutive cells along each axis, in cells");

    // the number of axes
    cls.def_property_readonly(
        // the name
        "rank",
        // the getter
        &Grid::rank,
        // the docstring
        "my number of axes");

    // whether my cells may be written
    cls.def_property_readonly(
        // the name
        "writable",
        // the getter
        &Grid::writable,
        // the docstring
        "whether python may write through to my cells");

    // the storage strategy that backs me
    cls.def_property_readonly(
        // the name
        "strategy",
        // the getter
        &Grid::strategy,
        // the docstring
        "the storage strategy that holds my cells");

    // the factory that allocates a fresh heap grid
    grid.def(
        // the name
        "heap",
        // the implementation
        &heap,
        // the signature
        "shape"_a, "dtype"_a,
        // the docstring
        "make a grid over a fresh block of heap memory of the given {shape} and {dtype}");

    // all done
    return;
}


// end of file
