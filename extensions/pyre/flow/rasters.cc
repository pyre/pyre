// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// helpers
namespace pyre::py::flow {
    // bind the rasters over cells of type {cellT}, and register them with the catalog
    template <typename cellT>
    inline void bindRaster(py::module & m)
    {
        // the raster
        using raster_type = raster_t<cellT>;
        // register it with the catalog, which describes it but cannot make one
        registry().registerProduct<raster_type>();
        // its readable name, which must outlive the binding of the class
        auto name = raster_type::className();
        // bind it
        auto cls = py::classh<raster_type, product_t>(
            // the scope
            m,
            // the name of the class
            name.c_str(),
            // the docstring
            "a tile over cells that live in a python buffer");
        // its shape
        cls.def_property_readonly(
            // the name
            "shape",
            // the implementation
            [](const raster_type & self) -> std::tuple<int, int> {
                // get the shape
                auto shape = self.shape();
                // and hand off its extents
                return { shape[0], shape[1] };
            },
            // the docstring
            "my shape");
        // all done
        return;
    }

    // make a raster over the cells described by {info}, if they are of type {cellT}
    template <typename cellT>
    inline auto makeRaster(const py::buffer_info & info, const string_t & name)
        -> std::shared_ptr<product_t>
    {
        // a buffer of some other cell type, or in a foreign byte order
        if (!info.item_type_is_equivalent_to<cellT>()) {
            // is not mine
            return nullptr;
        }
        // a buffer whose cells do not sit on their alignment cannot be read through {cellT}
        if (reinterpret_cast<std::uintptr_t>(info.ptr) % alignof(cellT) != 0) {
            // so refuse it
            throw py::value_error("the cells of '" + name + "' are not aligned");
        }
        // the extents and the strides, in cells; a band of a larger block arrives with strides
        // that step over the cells of its neighbors, so the layout must honor them
        auto shape = packing_t::shape_type {};
        auto strides = packing_t::strides_type {};
        // the span of the block the layout reaches, in cells
        packing_t::difference_type span = 1;
        // go through the axes
        for (int axis = 0; axis < 2; ++axis) {
            // the extent
            shape[axis] = info.shape[axis];
            // the stride, which the buffer reports in bytes
            strides[axis] = info.strides[axis] / static_cast<py::ssize_t>(info.itemsize);
            // fold the reach of this axis into the span
            span += (shape[axis] - 1) * strides[axis];
        }
        // the layout, with the origin at zero, visited in row major order
        auto packing =
            packing_t(shape, packing_t::index_type::zero(), packing_t::order_type::c(), strides, 0);
        // the cells, which the buffer owns
        auto storage = pyre::memory::constview_t<cellT>(static_cast<const cellT *>(info.ptr), span);
        // the raster over them
        return raster_t<cellT>::create(name, viewgrid_t<cellT>(packing, storage));
    }
} // namespace pyre::py::flow


// the rasters
void
pyre::py::flow::rasters(py::module & m)
{
    // signed integers
    bindRaster<pyre::memory::int8_t>(m);
    bindRaster<pyre::memory::int16_t>(m);
    bindRaster<pyre::memory::int32_t>(m);
    bindRaster<pyre::memory::int64_t>(m);
    // unsigned integers
    bindRaster<pyre::memory::uint8_t>(m);
    bindRaster<pyre::memory::uint16_t>(m);
    bindRaster<pyre::memory::uint32_t>(m);
    bindRaster<pyre::memory::uint64_t>(m);
    // floating point
    bindRaster<pyre::memory::float32_t>(m);
    bindRaster<pyre::memory::float64_t>(m);
    // complex
    bindRaster<pyre::memory::complex64_t>(m);
    bindRaster<pyre::memory::complex128_t>(m);

    // make a raster over the cells of a python buffer
    m.def(
        // the name
        "raster",
        // the implementation
        [](const py::buffer & source, const string_t & name) -> std::shared_ptr<product_t> {
            // describe the buffer
            auto info = source.request();
            // a raster has two axes
            if (info.ndim != 2) {
                // so refuse anything else
                throw py::value_error("a raster needs a buffer with two axes");
            }
            // try the cell types, one at a time
            for (auto raster : {
                     makeRaster<pyre::memory::int8_t>(info, name),
                     makeRaster<pyre::memory::int16_t>(info, name),
                     makeRaster<pyre::memory::int32_t>(info, name),
                     makeRaster<pyre::memory::int64_t>(info, name),
                     makeRaster<pyre::memory::uint8_t>(info, name),
                     makeRaster<pyre::memory::uint16_t>(info, name),
                     makeRaster<pyre::memory::uint32_t>(info, name),
                     makeRaster<pyre::memory::uint64_t>(info, name),
                     makeRaster<pyre::memory::float32_t>(info, name),
                     makeRaster<pyre::memory::float64_t>(info, name),
                     makeRaster<pyre::memory::complex64_t>(info, name),
                     makeRaster<pyre::memory::complex128_t>(info, name),
                 }) {
                // the one that fits
                if (raster) {
                    // is the answer
                    return raster;
                }
            }
            // a buffer of any other cell type has no raster
            throw py::value_error("the cells of '" + name + "' are of an unsupported type");
        },
        // the signature
        "source"_a, "name"_a,
        // the raster keeps the buffer, which owns its cells, alive
        py::keep_alive<0, 1>(),
        // the docstring
        "make a raster over the cells of {source}, a buffer with two axes, which it shares "
        "rather than copies");

    // all done
    return;
}


// end of file
