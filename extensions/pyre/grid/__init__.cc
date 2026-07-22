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
// the erased grid and its converters
#include "Grid.h"


// the erased grid measures with a signed integer, matching the c++ library
using size_type = pyre::py::grid::Grid::size_type;


// the factories all build over a runtime-rank packing, so that they dispatch on the cell type
// alone: twelve leaf instantiations per storage strategy, never a span of ranks as well
namespace pyre::py::grid {
    // the runtime-rank packing
    using packing_t = pyre::grid::dynamic_canonical_t;
    // its shape carries one signed extent per axis
    using shape_t = packing_t::shape_type;

    // choose a cell type from its pyre memory cell name and hand it to a callable that is
    // templated on that type; this keeps the twelve-way dispatch in one place
    template <class F>
    auto dispatchCell(const string_t & cell, F && f) -> Grid
    {
        // signed integers
        if (cell == "int8")
            return f.template operator()<pyre::memory::int8_t>();
        if (cell == "int16")
            return f.template operator()<pyre::memory::int16_t>();
        if (cell == "int32")
            return f.template operator()<pyre::memory::int32_t>();
        if (cell == "int64")
            return f.template operator()<pyre::memory::int64_t>();
        // unsigned integers
        if (cell == "uint8")
            return f.template operator()<pyre::memory::uint8_t>();
        if (cell == "uint16")
            return f.template operator()<pyre::memory::uint16_t>();
        if (cell == "uint32")
            return f.template operator()<pyre::memory::uint32_t>();
        if (cell == "uint64")
            return f.template operator()<pyre::memory::uint64_t>();
        // floating point
        if (cell == "float32")
            return f.template operator()<pyre::memory::float32_t>();
        if (cell == "float64")
            return f.template operator()<pyre::memory::float64_t>();
        // complex
        if (cell == "complex64")
            return f.template operator()<pyre::memory::complex64_t>();
        if (cell == "complex128")
            return f.template operator()<pyre::memory::complex128_t>();

        // anything else is a caller mistake
        auto channel = pyre::journal::error_t("pyre.grid.bindings");
        // complain
        channel << "unsupported grid cell type '" << cell << "'" << pyre::journal::endl(__HERE__);
        // and refuse
        throw py::value_error("unsupported grid cell type '" + cell + "'");
    }


    // a heap grid: allocate a fresh block of {shape} cells of type {cellT}
    template <class cellT>
    auto makeHeap(const shape_t & shape) -> Grid
    {
        // the storage and the grid over it
        using storage_t = pyre::memory::heap_t<cellT>;
        using grid_t = pyre::grid::grid_t<packing_t, storage_t>;
        // lay out the shape
        auto packing = packing_t(shape);
        // put enough cells on the heap
        auto storage = storage_t { packing.cells() };
        // make the grid and erase it; heap storage owns its cells
        return erase(grid_t { packing, storage }, "heap");
    }

    // the heap factory python calls
    auto heap(const std::vector<size_type> & extents, const string_t & cell) -> Grid
    {
        // adopt the extents as a shape
        auto shape = shape_t(extents.begin(), extents.end());
        // dispatch on the cell type
        return dispatchCell(cell, [&]<class T>() { return makeHeap<T>(shape); });
    }


    // a file-backed grid: lay {shape} cells of {cellT} over the product at {uri}
    // {create} chooses between making a fresh product sized to the shape, and mapping an
    // existing one, which is how a data product on disk is read back
    template <class cellT>
    auto makeMap(const string_t & uri, const shape_t & shape, bool create) -> Grid
    {
        // the storage and the grid over it
        using storage_t = pyre::memory::map_t<cellT>;
        using grid_t = pyre::grid::grid_t<packing_t, storage_t>;
        // lay out the shape
        auto packing = packing_t(shape);
        // either make a file large enough to hold the grid, or map an existing one for writing
        auto storage =
            create ? storage_t::create(uri, packing.cells()) : storage_t::open(uri, true);
        // make the grid and erase it; map storage owns its cells through a shared handle
        return erase(grid_t { packing, storage }, "map");
    }

    // the map factory python calls
    auto map(
        const string_t & uri, const std::vector<size_type> & extents, const string_t & cell,
        bool create) -> Grid
    {
        // adopt the extents as a shape
        auto shape = shape_t(extents.begin(), extents.end());
        // dispatch on the cell type
        return dispatchCell(cell, [&]<class T>() { return makeMap<T>(uri, shape, create); });
    }


    // a non-owning grid over memory python already holds: lay a {shape} of {cellT} cells over the
    // block the {source} buffer exports, without copying
    template <class cellT>
    auto makeView(const py::buffer & source, const shape_t & shape) -> Grid
    {
        // the storage and the grid over it
        using storage_t = pyre::memory::view_t<cellT>;
        using grid_t = pyre::grid::grid_t<packing_t, storage_t>;
        // lay out the shape
        auto packing = packing_t(shape);
        // the number of cells the grid needs
        auto cells = packing.cells();

        // ask the source for writable access to its block
        auto info = std::make_shared<py::buffer_info>(source.request(true));
        // the block must be at least as large as the grid
        if (info->size < cells) {
            // otherwise the caller has made a mistake
            throw py::value_error("source buffer is too small for the requested grid shape");
        }
        // and its cells must be the width we were told to expect
        if (info->itemsize != static_cast<py::ssize_t>(sizeof(cellT))) {
            // otherwise the cell and the buffer disagree
            throw py::value_error("source buffer cell size does not match the requested cell");
        }

        // a view over the source's memory
        auto storage = storage_t(static_cast<cellT *>(info->ptr), cells);
        // paired with the layout
        auto grid = grid_t { packing, storage };
        // the view owns nothing, so keep the source's buffer view open for as long as python
        // holds the erased grid; that pins both the exporter and its block
        return describe(grid, "view", info->ptr, info);
    }

    // the view factory python calls
    auto view(
        const py::buffer & source, const std::vector<size_type> & extents, const string_t & cell)
        -> Grid
    {
        // adopt the extents as a shape
        auto shape = shape_t(extents.begin(), extents.end());
        // dispatch on the cell type
        return dispatchCell(cell, [&]<class T>() { return makeView<T>(source, shape); });
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

    // the single erased grid class, presenting the python buffer protocol so any consumer of that
    // protocol can view its cells with no copy
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
        "shape"_a, "cell"_a,
        // the docstring
        "make a grid over a fresh block of heap memory of the given {shape} and {cell}");

    // the factory that maps a file-backed grid
    grid.def(
        // the name
        "map",
        // the implementation
        &map,
        // the signature; {create} makes a fresh product, else an existing one is mapped for
        // writing, which is how a data product on disk is read back
        "uri"_a, "shape"_a, "cell"_a, "create"_a = true,
        // the docstring
        "lay a grid of the given {shape} and {cell} over the memory-mapped file at {uri}");

    // the factory that wraps memory python already holds
    grid.def(
        // the name
        "view",
        // the implementation
        &view,
        // the signature
        "source"_a, "shape"_a, "cell"_a,
        // the docstring
        "lay a grid of the given {shape} and {cell} over the memory of the {source} buffer, "
        "without copying");

    // all done
    return;
}


// end of file
