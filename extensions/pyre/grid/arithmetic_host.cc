// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include <complex>
#include <stdexcept>
// the shared engine
#include "arithmetic.icc"


// the host half of the elementwise engine
namespace pyre::py::grid::arithmetic {
    namespace {
        // call {f} with the host type of a cell
        template <class F>
        inline auto
        withCell(cell_t cell, F && f) -> void
        {
            switch (cell) {
                case cell_t::int8:
                    return f.template operator()<std::int8_t>();
                case cell_t::int16:
                    return f.template operator()<std::int16_t>();
                case cell_t::int32:
                    return f.template operator()<std::int32_t>();
                case cell_t::int64:
                    return f.template operator()<std::int64_t>();
                case cell_t::uint8:
                    return f.template operator()<std::uint8_t>();
                case cell_t::uint16:
                    return f.template operator()<std::uint16_t>();
                case cell_t::uint32:
                    return f.template operator()<std::uint32_t>();
                case cell_t::uint64:
                    return f.template operator()<std::uint64_t>();
                case cell_t::float32:
                    return f.template operator()<float>();
                case cell_t::float64:
                    return f.template operator()<double>();
                case cell_t::complex64:
                    return f.template operator()<std::complex<float>>();
                case cell_t::complex128:
                    return f.template operator()<std::complex<double>>();
            }
            throw std::logic_error("arithmetic: unknown cell type");
        }
    } // namespace


    // {self op= other}, cell by cell
    auto
    host(op_t op, cell_t cell, const layout_t & self, const layout_t & other) -> void
    {
        withCell(cell, [&]<class T>() {
            withOp(op, [&](auto tag) {
                auto * a = static_cast<T *>(self.data);
                auto * b = static_cast<const T *>(other.data);
                for (std::int64_t k = 0; k < self.cells; ++k) {
                    apply<decltype(tag)::value>(a[offset(self, k)], b[offset(other, k)]);
                }
            });
        });
    }


    // {self op= scalar}, cell by cell
    auto
    host(op_t op, cell_t cell, const layout_t & self, const scalar_t & other) -> void
    {
        withCell(cell, [&]<class T>() {
            withOp(op, [&](auto tag) {
                auto * a = static_cast<T *>(self.data);
                auto b = value<T>(other);
                for (std::int64_t k = 0; k < self.cells; ++k) {
                    apply<decltype(tag)::value>(a[offset(self, k)], b);
                }
            });
        });
    }
} // namespace pyre::py::grid::arithmetic


// end of file
