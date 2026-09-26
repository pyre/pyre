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
// the type-erased grid and its converters, from the library's python-support tier
#include <pyre/py/grid/AnyGrid.h>
// and the type-erased mosaic, its out-of-core sibling
#include <pyre/py/grid/AnyMosaic.h>
// in-place elementwise arithmetic
#include "arithmetic.h"

// the cuda storage strategies, when built with cuda support
#ifdef WITH_CUDA
#include <pyre/cuda/memory.h>
#endif


// the type-erased grid measures with a signed integer, matching the c++ library
using size_type = pyre::py::grid::AnyGrid::size_type;


// the factories all build over a runtime-rank packing, so that they dispatch on the cell type
// alone: twelve leaf instantiations per storage strategy, never a span of ranks as well
namespace pyre::py::grid {
    // the runtime-rank packing
    using packing_t = pyre::grid::dynamic_canonical_t;
    // its shape carries one signed extent per axis
    using shape_t = packing_t::shape_type;

    // choose a native cell type from its pyre memory cell name and hand it to a callable that
    // is templated on that type; this keeps the twelve-way dispatch in one place, and the
    // return type is deduced so both grid and mosaic factories can ride it; {requested} is the
    // name the caller actually used, for the complaint
    template <class F>
    auto dispatchBase(const string_t & cell, const string_t & requested, F && f)
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

        // anything else is a caller mistake; refuse it the way the other factories refuse bad
        // arguments, with a python exception and no journal entry, since a fatal error channel
        // would preempt the exception
        throw py::value_error("unsupported grid cell type '" + requested + "'");
    }

    // choose a cell type from its name, honoring a trailing byte order marker: {float64be} is a
    // big endian double, {uint16le} a little endian unsigned short; a marker that names the
    // host's own order collapses to the native cell, so only foreign order data pays for the
    // wrapper
    template <class F>
    auto dispatchCell(const string_t & cell, F && f)
    {
        // the marker is the last two characters, if there is room for a base name before them
        if (cell.size() > 2) {
            // split the name
            auto base = cell.substr(0, cell.size() - 2);
            auto marker = cell.substr(cell.size() - 2);
            // big endian
            if (marker == "be") {
                // wrap the base cell in the big endian spelling
                return dispatchBase(base, cell, [&]<class T>() {
                    return f.template operator()<pyre::memory::big_t<T>>();
                });
            }
            // little endian
            if (marker == "le") {
                // wrap the base cell in the little endian spelling
                return dispatchBase(base, cell, [&]<class T>() {
                    return f.template operator()<pyre::memory::little_t<T>>();
                });
            }
        }
        // no marker: the name is a native cell
        return dispatchBase(cell, cell, std::forward<F>(f));
    }


    // a heap grid: allocate a fresh block of {shape} cells of type {cellT}
    template <class cellT>
    auto makeHeap(const shape_t & shape) -> AnyGrid
    {
        // the storage and the grid over it
        using storage_t = pyre::memory::heap_t<cellT>;
        using grid_t = pyre::grid::grid_t<packing_t, storage_t>;
        // lay out the shape
        auto packing = packing_t(shape);
        // put enough cells on the heap
        auto storage = storage_t { packing.cells() };
        // make the grid and type-erase it; heap storage owns its cells
        return anyGrid(grid_t { packing, storage }, "heap");
    }

    // the heap factory python calls
    auto heap(const std::vector<size_type> & extents, const string_t & cell) -> AnyGrid
    {
        // adopt the extents as a shape
        auto shape = shape_t(extents.begin(), extents.end());
        // dispatch on the cell type
        return dispatchCell(cell, [&]<class T>() { return makeHeap<T>(shape); });
    }


#ifdef WITH_CUDA
    // a managed grid: allocate a fresh block of {shape} cells of type {cellT} on cuda managed
    // (unified) memory, accessible from both the host and whichever device is current
    template <class cellT>
    auto makeManaged(const shape_t & shape) -> AnyGrid
    {
        // the storage and the grid over it
        using storage_t = pyre::cuda::memory::managed_t<cellT>;
        using grid_t = pyre::grid::grid_t<packing_t, storage_t>;
        // lay out the shape
        auto packing = packing_t(shape);
        // put enough cells on managed memory
        auto storage = storage_t { packing.cells() };
        // make the grid and type-erase it; managed storage owns its cells, exactly like heap
        return anyGrid(grid_t { packing, storage }, "managed");
    }

    // the managed factory python calls
    auto managed(const std::vector<size_type> & extents, const string_t & cell) -> AnyGrid
    {
        // adopt the extents as a shape
        auto shape = shape_t(extents.begin(), extents.end());
        // dispatch on the cell type
        return dispatchCell(cell, [&]<class T>() { return makeManaged<T>(shape); });
    }
#endif


    // a file-backed grid: lay {shape} cells of {cellT} over the product at {uri}
    // {create} chooses between making a fresh product sized to the shape, and mapping an
    // existing one, which is how a data product on disk is read back
    template <class cellT>
    auto makeMap(const string_t & uri, const shape_t & shape, bool create) -> AnyGrid
    {
        // the storage and the grid over it
        using storage_t = pyre::memory::map_t<cellT>;
        using grid_t = pyre::grid::grid_t<packing_t, storage_t>;
        // lay out the shape
        auto packing = packing_t(shape);
        // either make a file large enough to hold the grid, or map an existing one for writing
        auto storage =
            create ? storage_t::create(uri, packing.cells()) : storage_t::open(uri, true);
        // make the grid and type-erase it; map storage owns its cells through a shared handle
        return anyGrid(grid_t { packing, storage }, "map");
    }

    // a read-only file-backed grid: map the product at {uri} without write access, which is
    // how a client examines a data product it does not own
    template <class cellT>
    auto makeConstMap(const string_t & uri, const shape_t & shape) -> AnyGrid
    {
        // the storage and the grid over it
        using storage_t = pyre::memory::constmap_t<cellT>;
        using grid_t = pyre::grid::grid_t<packing_t, storage_t>;
        // lay out the shape
        auto packing = packing_t(shape);
        // map the existing product for reading only
        auto storage = storage_t::open(uri);
        // make the grid and type-erase it; the const cells mark the description read-only
        return anyGrid(grid_t { packing, storage }, "map");
    }

    // the map factory python calls
    auto map(
        const string_t & uri, const std::vector<size_type> & extents, const string_t & cell,
        bool create, bool writable) -> AnyGrid
    {
        // a fresh product exists to be filled, so refusing write access to it is a mistake
        if (create && !writable) {
            // complain
            throw py::value_error(
                "a fresh product must be writable; open an existing one "
                "with {create=False} for read-only access");
        }
        // adopt the extents as a shape
        auto shape = shape_t(extents.begin(), extents.end());
        // for read-only access
        if (!writable) {
            // dispatch to the const flavor
            return dispatchCell(cell, [&]<class T>() { return makeConstMap<T>(uri, shape); });
        }
        // otherwise, dispatch to the writable one
        return dispatchCell(cell, [&]<class T>() { return makeMap<T>(uri, shape, create); });
    }


    // a non-owning grid over memory python already holds: lay a {shape} of {cellT} cells over the
    // block the {source} buffer exports, without copying
    template <class cellT>
    auto makeView(const py::buffer & source, const shape_t & shape) -> AnyGrid
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
        // holds the type-erased grid; that pins both the exporter and its block
        return describe(grid, "view", info->ptr, info);
    }

    // a read-only view over memory python already holds: the counterpart of {makeView} for
    // sources that refuse write access, such as {bytes}
    template <class cellT>
    auto makeConstView(const py::buffer & source, const shape_t & shape) -> AnyGrid
    {
        // the storage and the grid over it
        using storage_t = pyre::memory::constview_t<cellT>;
        using grid_t = pyre::grid::grid_t<packing_t, storage_t>;
        // lay out the shape
        auto packing = packing_t(shape);
        // the number of cells the grid needs
        auto cells = packing.cells();

        // ask the source for read access to its block
        auto info = std::make_shared<py::buffer_info>(source.request(false));
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

        // a read-only view over the source's memory
        auto storage = storage_t(static_cast<const cellT *>(info->ptr), cells);
        // paired with the layout
        auto grid = grid_t { packing, storage };
        // the view owns nothing, so keep the source's buffer view open for as long as python
        // holds the type-erased grid; that pins both the exporter and its block
        return describe(grid, "view", info->ptr, info);
    }

    // the view factory python calls
    auto view(
        const py::buffer & source, const std::vector<size_type> & extents, const string_t & cell,
        bool writable) -> AnyGrid
    {
        // adopt the extents as a shape
        auto shape = shape_t(extents.begin(), extents.end());
        // for read-only access
        if (!writable) {
            // dispatch to the const flavor, which asks the source for read access only
            return dispatchCell(cell, [&]<class T>() { return makeConstView<T>(source, shape); });
        }
        // otherwise, dispatch to the writable one
        return dispatchCell(cell, [&]<class T>() { return makeView<T>(source, shape); });
    }


    // a mosaic: an out-of-core grid of {shape} cells of {cellT}, diced into tiles of extent
    // {tile}, over a store with one demand-materialized page per tile
    template <class cellT>
    auto makeMosaic(const shape_t & shape, const shape_t & tile, const string_t & cell) -> AnyMosaic
    {
        // the tiled layout, the storage, and the grid over them
        using chunked_t = pyre::grid::dynamic_chunked_t;
        using storage_t = pyre::memory::paged_t<cellT>;
        using grid_t = pyre::grid::grid_t<chunked_t, storage_t>;
        // dice the box
        auto packing = chunked_t(shape, tile);
        // a page holds a full tile's worth of cells
        typename storage_t::cell_count_type pageCells = 1;
        // measured axis by axis
        for (auto extent : packing.tileShape()) {
            // as the volume of one tile
            pageCells *= extent;
        }
        // and there is one page per tile
        typename storage_t::cell_count_type pages = 1;
        // likewise
        for (auto extent : packing.tiles()) {
            // the volume of the tile grid
            pages *= extent;
        }
        // make a store with nothing resident: describing the product is free, and pages get
        // allocated only as python touches their tiles
        auto storage = storage_t { pageCells, pages };
        // assemble the mosaic and type-erase it
        return anyMosaic(grid_t { packing, storage }, cell);
    }

    // the mosaic factory python calls
    auto mosaic(
        const std::vector<size_type> & extents, const std::vector<size_type> & tile,
        const string_t & cell) -> AnyMosaic
    {
        // adopt the extents as shapes
        auto shape = shape_t(extents.begin(), extents.end());
        auto tileShape = shape_t(tile.begin(), tile.end());
        // dispatch on the cell type
        return dispatchCell(cell, [&]<class T>() { return makeMosaic<T>(shape, tileShape, cell); });
    }


    // in-place arithmetic: translate python operands into descriptions the elementwise engine
    // understands, and send them to the half that can reach the target's cells
    namespace inplace {
        // the engine
        namespace arith = pyre::py::grid::arithmetic;

        // the engine's name for a cell type, from its buffer protocol format
        inline auto cell(string_t format) -> arith::cell_t
        {
            // a byte order marker only makes sense for the host's own order
            if (!format.empty() && (format.front() == '<' || format.front() == '>')) {
                // the order the host spells
                const char native = std::endian::native == std::endian::big ? '>' : '<';
                // a foreign order would need byte swapping
                if (format.front() != native) {
                    throw py::type_error("grid arithmetic: cells in foreign byte order");
                }
                // otherwise, drop the marker
                format.erase(0, 1);
            }
            if (format == "b") return arith::cell_t::int8;
            if (format == "h") return arith::cell_t::int16;
            if (format == "i") return arith::cell_t::int32;
            if (format == "q" || format == "l") return arith::cell_t::int64;
            if (format == "B") return arith::cell_t::uint8;
            if (format == "H") return arith::cell_t::uint16;
            if (format == "I") return arith::cell_t::uint32;
            if (format == "Q" || format == "L") return arith::cell_t::uint64;
            if (format == "f") return arith::cell_t::float32;
            if (format == "d") return arith::cell_t::float64;
            if (format == "Zf") return arith::cell_t::complex64;
            if (format == "Zd") return arith::cell_t::complex128;
            throw py::type_error("grid arithmetic: unsupported cell format '" + format + "'");
        }

        // the three families of cell types
        inline auto isInteger(arith::cell_t c) -> bool { return c <= arith::cell_t::uint64; }
        inline auto isComplex(arith::cell_t c) -> bool { return c >= arith::cell_t::complex64; }

        // describe a grid's cells as a layout
        inline auto layout(const py::buffer_info & info) -> arith::layout_t
        {
            // make sure the engine can hold the rank
            if (info.ndim > arith::maxRank) {
                throw py::value_error(
                    "grid arithmetic: at most " + std::to_string(arith::maxRank) + " axes");
            }
            // fill in the description
            auto result = arith::layout_t {};
            result.data = info.ptr;
            result.rank = static_cast<int>(info.ndim);
            result.cells = 1;
            result.contiguous = true;
            // the stride a packed row major layout would have, walking from the fastest axis
            std::int64_t packed = 1;
            for (auto axis = info.ndim; axis-- > 0;) {
                result.shape[axis] = info.shape[axis];
                // the buffer protocol measures strides in bytes; the engine, in cells
                result.strides[axis] = info.strides[axis] / info.itemsize;
                result.cells *= info.shape[axis];
                // an axis of extent one doesn't care about its stride
                if (info.shape[axis] > 1 && result.strides[axis] != packed) {
                    result.contiguous = false;
                }
                packed *= info.shape[axis];
            }
            return result;
        }

        // whether cuda can reach a grid's cells
        inline auto onDevice(const AnyGrid & grid) -> bool
        {
            return grid.strategy() == "managed" || grid.strategy() == "pinned";
        }

        // whether two layouts reach any of the same bytes without describing the same cells;
        // elementwise work over such a pair would read cells another thread has already written
        inline auto overlap(
            const arith::layout_t & a, const arith::layout_t & b, std::int64_t itemsize) -> bool
        {
            // empty grids reach nothing
            if (a.cells == 0 || b.cells == 0) {
                return false;
            }
            // the same view of the same cells is fine: each cell only ever meets itself
            bool same = a.data == b.data;
            for (int axis = 0; same && axis < a.rank; ++axis) {
                same = a.strides[axis] == b.strides[axis];
            }
            if (same) {
                return false;
            }
            // the range of bytes a layout reaches
            auto span = [itemsize](const arith::layout_t & l) {
                auto lo = static_cast<const char *>(l.data);
                auto hi = lo;
                for (int axis = 0; axis < l.rank; ++axis) {
                    auto reach = (l.shape[axis] - 1) * l.strides[axis] * itemsize;
                    (reach < 0 ? lo : hi) += reach;
                }
                return std::pair { lo, hi + itemsize };
            };
            auto [alo, ahi] = span(a);
            auto [blo, bhi] = span(b);
            return alo < bhi && blo < ahi;
        }

        // the range of an integer cell type, as python integers so the comparison is exact
        inline auto bounds(arith::cell_t c) -> std::pair<py::int_, py::int_>
        {
            // the unsigned types start at zero
            using ull = unsigned long long;
            switch (c) {
                case arith::cell_t::int8: return { py::int_(INT8_MIN), py::int_(INT8_MAX) };
                case arith::cell_t::int16: return { py::int_(INT16_MIN), py::int_(INT16_MAX) };
                case arith::cell_t::int32: return { py::int_(INT32_MIN), py::int_(INT32_MAX) };
                case arith::cell_t::int64: return { py::int_(INT64_MIN), py::int_(INT64_MAX) };
                case arith::cell_t::uint8: return { py::int_(0), py::int_(ull { UINT8_MAX }) };
                case arith::cell_t::uint16: return { py::int_(0), py::int_(ull { UINT16_MAX }) };
                case arith::cell_t::uint32: return { py::int_(0), py::int_(ull { UINT32_MAX }) };
                default: return { py::int_(0), py::int_(ull { UINT64_MAX }) };
            }
        }

        // translate a python scalar for a target of cell type {c}; {false} if it isn't a scalar
        // this knows about, in which case python gets to try something else
        inline auto scalar(const py::handle & value, arith::cell_t c, arith::scalar_t & result)
            -> bool
        {
            // complex numbers fit complex cells only
            if (PyComplex_Check(value.ptr())) {
                if (!isComplex(c)) {
                    throw py::type_error(
                        "grid arithmetic: a complex scalar needs a grid of complex cells");
                }
                result.re = PyComplex_RealAsDouble(value.ptr());
                result.im = PyComplex_ImagAsDouble(value.ptr());
                return true;
            }
            // floats fit floating point and complex cells
            if (PyFloat_Check(value.ptr())) {
                if (isInteger(c)) {
                    throw py::type_error(
                        "grid arithmetic: a float scalar would lose its fraction in a grid of "
                        "integer cells");
                }
                result.re = PyFloat_AsDouble(value.ptr());
                return true;
            }
            // integers, including anything that behaves like one, fit every cell type
            if (PyIndex_Check(value.ptr())) {
                auto number = py::reinterpret_steal<py::int_>(PyNumber_Index(value.ptr()));
                if (!isInteger(c)) {
                    result.re = PyLong_AsDouble(number.ptr());
                    return true;
                }
                // as long as they are in range, like numpy has them be
                auto [lo, hi] = bounds(c);
                if (number < lo || number > hi) {
                    throw py::value_error(
                        "grid arithmetic: " + py::str(number).cast<string_t>()
                        + " is out of range for the grid's cells");
                }
                // store both spellings; the engine picks the one the cell type wants
                if (number < py::int_(0)) {
                    result.i = number.cast<long long>();
                    result.u = static_cast<std::uint64_t>(result.i);
                } else {
                    result.u = number.cast<unsigned long long>();
                    result.i = static_cast<std::int64_t>(result.u);
                }
                return true;
            }
            // anything else is not mine to handle
            return false;
        }

        // {self op= other}
        inline auto apply(py::object self, py::object other, arith::op_t op) -> py::object
        {
            // the target
            auto & target = self.cast<AnyGrid &>();
            // must be writable
            if (!target.writable()) {
                throw py::value_error("grid arithmetic: this grid is read-only");
            }
            // describe it
            auto info = target.view();
            auto c = cell(info.format);
            auto a = layout(info);
            // integer cells can't hold a quotient
            if (op == arith::op_t::div && isInteger(c)) {
                throw py::type_error(
                    "grid arithmetic: in-place division would lose the fraction in a grid of "
                    "integer cells");
            }
            // where the work happens is decided by where the target's cells live
            bool device = onDevice(target);

            // a grid on the right
            if (py::isinstance<AnyGrid>(other)) {
                auto & source = other.cast<AnyGrid &>();
                auto sinfo = source.view();
                // must hold the same kind of cells
                if (cell(sinfo.format) != c) {
                    throw py::type_error(
                        "grid arithmetic: the grids hold different cell types, '" + info.format
                        + "' and '" + sinfo.format + "'");
                }
                auto b = layout(sinfo);
                // in the same shape
                bool shaped = a.rank == b.rank;
                for (int axis = 0; shaped && axis < a.rank; ++axis) {
                    shaped = a.shape[axis] == b.shape[axis];
                }
                if (!shaped) {
                    throw py::value_error("grid arithmetic: the grids have different shapes");
                }
                // without stepping on each other
                if (overlap(a, b, info.itemsize)) {
                    throw py::value_error(
                        "grid arithmetic: the grids share cells in different places; copy one "
                        "of them first");
                }
                // the device can't reach host-only cells
                if (device && !onDevice(source)) {
                    throw py::type_error(
                        "grid arithmetic: a grid on '" + target.strategy()
                        + "' storage can't take a grid on '" + source.strategy()
                        + "' storage, whose cells the device can't reach");
                }
#ifdef WITH_CUDA
                // on the device, without waiting
                if (device) {
                    arith::device(op, c, a, b);
                    return self;
                }
                // the host is about to read cells the device may still be writing
                if (onDevice(source)) {
                    arith::synchronize();
                }
#endif
                // on the host
                arith::host(op, c, a, b);
                return self;
            }

            // a scalar on the right
            auto s = arith::scalar_t {};
            if (!scalar(other, c, s)) {
                // not something i know how to combine with a grid
                return py::reinterpret_borrow<py::object>(Py_NotImplemented);
            }
#ifdef WITH_CUDA
            // on the device, without waiting
            if (device) {
                arith::device(op, c, a, s);
                return self;
            }
#endif
            // on the host
            arith::host(op, c, a, s);
            return self;
        }
    } // namespace inplace
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

    // the single type-erased grid class, presenting the python buffer protocol so any consumer of
    // that protocol can view its cells with no copy
    auto cls = py::class_<AnyGrid>(
        // in the submodule
        grid,
        // named
        "Grid",
        // exposing the buffer protocol
        py::buffer_protocol(),
        // the docstring
        "a multi-dimensional array whose cells live behind a storage strategy");

    // wire the buffer protocol to the type-erased grid's own description
    cls.def_buffer([](AnyGrid & self) -> py::buffer_info { return self.view(); });

    // the extent along each axis
    cls.def_property_readonly(
        // the name
        "shape",
        // the getter
        &AnyGrid::shape,
        // the docstring
        "my extent along each axis");

    // the strides, in cells
    cls.def_property_readonly(
        // the name
        "strides",
        // the getter
        &AnyGrid::strides,
        // the docstring
        "the distance between consecutive cells along each axis, in cells");

    // the number of axes
    cls.def_property_readonly(
        // the name
        "rank",
        // the getter
        &AnyGrid::rank,
        // the docstring
        "my number of axes");

    // whether my cells may be written
    cls.def_property_readonly(
        // the name
        "writable",
        // the getter
        &AnyGrid::writable,
        // the docstring
        "whether python may write through to my cells");

    // the storage strategy that backs me
    cls.def_property_readonly(
        // the name
        "strategy",
        // the getter
        &AnyGrid::strategy,
        // the docstring
        "the storage strategy that holds my cells");

    // the address of my first cell
    cls.def_property_readonly(
        // the name
        "address",
        // the getter
        &AnyGrid::address,
        // the docstring
        "the address of my first cell, as an integer, for code that takes raw pointers");

    // the cuda array interface, for consumers such as numba and cupy
    cls.def_property_readonly(
        // the name
        "__cuda_array_interface__",
        // the getter
        &AnyGrid::cudaArrayInterface,
        // the docstring
        "the version 3 cuda array interface description of my cells; only grids on cuda "
        "storage have one");

    // dlpack support: the device i live on, as the {(device_type, device_id)} pair the
    // protocol specifies
    cls.def(
        // the name
        "__dlpack_device__",
        // the implementation
        &AnyGrid::dlpackDevice,
        // the docstring
        "the (device_type, device_id) pair identifying where my cells live");

    // dlpack support: a capsule any consumer that speaks the protocol can import with no copy
    cls.def(
        // the name
        "__dlpack__",
        // the implementation; {stream}/{dl_device}/{copy} are accepted, as the protocol
        // requires, but not yet acted on -- i always hand back my own memory, on my own device;
        // {max_version} picks the flavor: consumers that ask for 1.0 or later get the versioned
        // tensor, and those that don't ask get the legacy one, per the protocol
        [](const AnyGrid & self, py::kwargs kwds) {
            // assume a consumer that predates versioning
            bool versioned = false;
            // unless it says otherwise
            if (kwds.contains("max_version") && !kwds["max_version"].is_none()) {
                // a {(major, minor)} pair; the versioned tensor is dlpack 1.0 and later
                auto version = kwds["max_version"].cast<py::tuple>();
                versioned = version.size() > 0 && version[0].cast<int>() >= 1;
            }
            // build the capsule
            return self.dlpack(versioned);
        },
        // the docstring
        "a dlpack capsule describing my cells, importable with no copy by numpy, pytorch, "
        "jax, cupy, or cuda.core alike");

    // read access: {g[i, j, ...]}
    cls.def(
        // the name
        "__getitem__",
        // the implementation
        &AnyGrid::getitem,
        // the signature
        "index"_a,
        // the docstring
        "the cell at a full index, or a sub-grid for a partial or sliced {index}");

    // write access: {g[i, j, ...] = v}
    cls.def(
        // the name
        "__setitem__",
        // the implementation
        &AnyGrid::setitem,
        // the signature
        "index"_a, "value"_a,
        // the docstring
        "write {value} into the cell at a full integer {index}");

    // in-place arithmetic, with a grid of the same shape and cell type or a scalar on the right;
    // grids on cuda storage do the work on the device, without waiting for it, and the rest on
    // the host
    using op_t = arithmetic::op_t;
    for (auto [name, op] : std::initializer_list<std::pair<const char *, op_t>> {
             { "__iadd__", op_t::add },
             { "__isub__", op_t::sub },
             { "__imul__", op_t::mul },
             { "__itruediv__", op_t::div },
         }) {
        cls.def(
            // the name
            name,
            // the implementation
            [op](py::object self, py::object other) { return inplace::apply(self, other, op); },
            // the signature
            "other"_a,
            // the docstring
            "combine {other}, a grid of my shape and cell type or a scalar, into my cells; on "
            "cuda storage the work is queued on the device, so synchronize before reading");
    }

#ifdef WITH_CUDA
    // wait for the device work in-place arithmetic has queued
    grid.def(
        // the name
        "synchronize",
        // the implementation
        &arithmetic::synchronize,
        // the docstring
        "wait for the device to finish the work queued on grids on cuda storage");
#endif

    // the type-erased mosaic: an out-of-core grid whose cells live on demand-materialized
    // pages, one per tile, reached tile by tile through zero-copy panes
    auto mos = py::class_<AnyMosaic>(
        // in the submodule
        grid,
        // named
        "Mosaic",
        // the docstring
        "an out-of-core grid whose tiles materialize on demand and travel as zero-copy panes");

    // the extent along each axis
    mos.def_property_readonly(
        // the name
        "shape",
        // the getter
        &AnyMosaic::shape,
        // the docstring
        "my extent along each axis");

    // the smallest addressable index
    mos.def_property_readonly(
        // the name
        "origin",
        // the getter
        &AnyMosaic::origin,
        // the docstring
        "my smallest addressable index");

    // the number of axes
    mos.def_property_readonly(
        // the name
        "rank",
        // the getter
        &AnyMosaic::rank,
        // the docstring
        "my number of axes");

    // the extent of the grid of tiles
    mos.def_property_readonly(
        // the name
        "tiles",
        // the getter
        &AnyMosaic::tiles,
        // the docstring
        "the extent of my grid of tiles");

    // the extent of one tile
    mos.def_property_readonly(
        // the name
        "tileShape",
        // the getter
        &AnyMosaic::tileShape,
        // the docstring
        "the extent of one of my tiles");

    // the storage bill
    mos.def_property_readonly(
        // the name
        "cells",
        // the getter
        &AnyMosaic::cells,
        // the docstring
        "the number of cells my storage supplies: every tile at full size, padding included");

    // the name of the cell type
    mos.def_property_readonly(
        // the name
        "cell",
        // the getter
        &AnyMosaic::cell,
        // the docstring
        "the name of my cell type");

    // the resident census
    mos.def_property_readonly(
        // the name
        "residents",
        // the getter
        &AnyMosaic::residents,
        // the docstring
        "the number of my pages that are actually resident");

    // the tile a given index falls in
    mos.def(
        // the name
        "tileOf",
        // the implementation
        &AnyMosaic::tileOf,
        // the signature
        "index"_a,
        // the docstring
        "the coordinates, in my grid of tiles, of the tile {index} falls in");

    // the working set of a window
    mos.def(
        // the name
        "tilesOverlapping",
        // the implementation
        &AnyMosaic::tilesOverlapping,
        // the signature
        "base"_a, "shape"_a,
        // the docstring
        "the tiles touched by the box anchored at {base} with the given {shape}");

    // the pane over a tile
    mos.def(
        // the name
        "pane",
        // the implementation
        &AnyMosaic::pane,
        // the signature
        "tile"_a,
        // the docstring
        "a dense zero-copy grid over the page that holds {tile}, materializing it on first "
        "touch");

    // read access: {m[i, j, ...]}
    mos.def(
        // the name
        "__getitem__",
        // the implementation
        &AnyMosaic::getitem,
        // the signature
        "index"_a,
        // the docstring
        "the cell at a full integer {index}; its page must be resident");

    // write access: {m[i, j, ...] = v}
    mos.def(
        // the name
        "__setitem__",
        // the implementation
        &AnyMosaic::setitem,
        // the signature
        "index"_a, "value"_a,
        // the docstring
        "write {value} into the cell at a full integer {index}, materializing its page on "
        "first touch and tainting it");

    // the page state probes
    mos.def(
        // the name
        "resident",
        // the implementation
        &AnyMosaic::resident,
        // the signature
        "tile"_a,
        // the docstring
        "whether the page that backs {tile} has been allocated");

    mos.def(
        // the name
        "valid",
        // the implementation
        &AnyMosaic::valid,
        // the signature
        "tile"_a,
        // the docstring
        "whether meaningful content has been deposited in {tile}");

    mos.def(
        // the name
        "clean",
        // the implementation
        &AnyMosaic::clean,
        // the signature
        "tile"_a,
        // the docstring
        "whether the content of {tile} matches my backing store");

    // and the page state marks
    mos.def(
        // the name
        "validate",
        // the implementation
        &AnyMosaic::validate,
        // the signature
        "tile"_a,
        // the docstring
        "record that meaningful content has been deposited in {tile}");

    mos.def(
        // the name
        "taint",
        // the implementation
        &AnyMosaic::taint,
        // the signature
        "tile"_a,
        // the docstring
        "record that {tile} has been written to, so it diverges from my backing store");

    mos.def(
        // the name
        "flush",
        // the implementation; the per-tile flavor, since an in-memory mosaic has no backing
        // store for the wholesale one to talk to
        py::overload_cast<const AnyMosaic::index_type &>(&AnyMosaic::flush, py::const_),
        // the signature
        "tile"_a,
        // the docstring
        "record that {tile} has been saved, so it matches my backing store again");

    mos.def(
        // the name
        "release",
        // the implementation
        &AnyMosaic::release,
        // the signature
        "tile"_a,
        // the docstring
        "let go of the page that backs {tile}, returning it to the never-touched state; "
        "outstanding panes keep their memory but no longer alias my cells");

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

#ifdef WITH_CUDA
    // the factory that allocates a fresh grid on cuda managed memory
    grid.def(
        // the name
        "managed",
        // the implementation
        &managed,
        // the signature
        "shape"_a, "cell"_a,
        // the docstring
        "make a grid over a fresh block of cuda managed (unified) memory of the given "
        "{shape} and {cell}, accessible from both the host and the current device");
#endif

    // the factory that maps a file-backed grid
    grid.def(
        // the name
        "map",
        // the implementation
        &map,
        // the signature; {create} makes a fresh product, else an existing one is mapped;
        // {writable} chooses between mapping it for writing and read-only access
        "uri"_a, "shape"_a, "cell"_a, "create"_a = true, "writable"_a = true,
        // the docstring
        "lay a grid of the given {shape} and {cell} over the memory-mapped file at {uri}");

    // the factory that wraps memory python already holds
    grid.def(
        // the name
        "view",
        // the implementation
        &view,
        // the signature; {writable} decides how much access to ask the source for, so
        // read-only exporters such as {bytes} are viewable with {writable=False}
        "source"_a, "shape"_a, "cell"_a, "writable"_a = true,
        // the docstring
        "lay a grid of the given {shape} and {cell} over the memory of the {source} buffer, "
        "without copying");

    // the factory that describes an out-of-core mosaic
    grid.def(
        // the name
        "mosaic",
        // the implementation
        &mosaic,
        // the signature
        "shape"_a, "tile"_a, "cell"_a,
        // the docstring
        "describe an out-of-core grid of the given {shape} and {cell}, diced into tiles of "
        "extent {tile}; nothing is allocated until a tile is touched");

    // all done
    return;
}


// end of file
