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
#include "engine.h"


// the host spelling of the cell types
namespace {
    // the arithmetic vocabulary
    namespace arithmetic = pyre::py::grid::arithmetic;

    // call {f} with the host type of the cells of type {cell}
    template <class functionT>
    auto withCell(arithmetic::Cell cell, functionT && f) -> void
    {
        // pick the cell type
        switch (cell) {
            // the signed integers
            case arithmetic::Cell::int8:
                return f.template operator()<std::int8_t>();
            case arithmetic::Cell::int16:
                return f.template operator()<std::int16_t>();
            case arithmetic::Cell::int32:
                return f.template operator()<std::int32_t>();
            case arithmetic::Cell::int64:
                return f.template operator()<std::int64_t>();
            // the unsigned integers
            case arithmetic::Cell::uint8:
                return f.template operator()<std::uint8_t>();
            case arithmetic::Cell::uint16:
                return f.template operator()<std::uint16_t>();
            case arithmetic::Cell::uint32:
                return f.template operator()<std::uint32_t>();
            case arithmetic::Cell::uint64:
                return f.template operator()<std::uint64_t>();
            // the floating point numbers
            case arithmetic::Cell::float32:
                return f.template operator()<float>();
            case arithmetic::Cell::float64:
                return f.template operator()<double>();
            // the complex numbers
            case arithmetic::Cell::complex64:
                return f.template operator()<std::complex<float>>();
            case arithmetic::Cell::complex128:
                return f.template operator()<std::complex<double>>();
        }
        // all done
        return;
    }
} // namespace


// make the cells within reach of the host
auto
pyre::py::grid::HostEngine::access() -> void
{
    // host cells are always within reach
    return;
}


// combine the cells of {source} into the cells of {target}
auto
pyre::py::grid::HostEngine::apply(
    arithmetic::Operation op, arithmetic::Cell cell, const arithmetic::Layout & target,
    const arithmetic::Layout & source) -> void
{
    // with the host type of the cells
    withCell(cell, [&]<class cellT>() {
        // and the operation fixed at compile time
        arithmetic::withOperation(op, [&](auto operation) {
            // the cells of the target
            auto * a = static_cast<cellT *>(target.data);
            // and of the source
            const auto * b = static_cast<const cellT *>(source.data);
            // visit them all
            for (std::int64_t k = 0; k < target.cells; ++k) {
                // and combine each pair
                arithmetic::apply<decltype(operation)::value>(
                    a[arithmetic::offset(target, k)], b[arithmetic::offset(source, k)]);
            }
        });
    });
    // all done
    return;
}


// combine {value} into the cells of {target}
auto
pyre::py::grid::HostEngine::apply(
    arithmetic::Operation op, arithmetic::Cell cell, const arithmetic::Layout & target,
    const arithmetic::Scalar & value) -> void
{
    // with the host type of the cells
    withCell(cell, [&]<class cellT>() {
        // and the operation fixed at compile time
        arithmetic::withOperation(op, [&](auto operation) {
            // the cells of the target
            auto * a = static_cast<cellT *>(target.data);
            // the value, as a cell
            const auto b = arithmetic::value<cellT>(value);
            // visit them all
            for (std::int64_t k = 0; k < target.cells; ++k) {
                // and combine each one with the value
                arithmetic::apply<decltype(operation)::value>(a[arithmetic::offset(target, k)], b);
            }
        });
    });
    // all done
    return;
}


// end of file
