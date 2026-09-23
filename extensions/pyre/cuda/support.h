// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// externals
#include "external.h"


// small shared support for the cublas/cusolver/curand bindings: none of it is specific to any
// one library, so it lives here rather than being repeated three times
namespace pyre::py::cuda {

    // a library handle (cublasHandle_t, cusolverDnHandle_t, curandGenerator_t, ...) is just an
    // opaque pointer; python holds it as the plain integer that pointer's bits spell, exactly
    // the way nvmath's own low-level bindings do, and hands it back on every call so there is
    // no hidden state on this side of the boundary
    template <class handleT>
    inline auto toHandle(std::uintptr_t handle) -> handleT
    {
        return reinterpret_cast<handleT>(handle);
    }

    // the reverse: publish a freshly allocated handle as the integer python will carry around
    template <class handleT>
    inline auto fromHandle(handleT handle) -> std::uintptr_t
    {
        return reinterpret_cast<std::uintptr_t>(handle);
    }

    // every routine below launches on the default stream and hands python back a grid it can
    // read immediately, cuda managed memory included; a launch is asynchronous, so a sync
    // after each call is what makes that promise true, and it is also where an asynchronous
    // launch failure actually surfaces
    inline auto
    checkCuda(cudaError_t status, const char * routine) -> void
    {
        if (status == cudaSuccess) {
            return;
        }
        throw std::runtime_error(std::string(routine) + ": " + cudaGetErrorString(status));
    }

    // synchronize the default stream and translate a launch failure into a python exception
    inline auto
    synchronize(const char * routine) -> void
    {
        checkCuda(cudaDeviceSynchronize(), routine);
    }

    // the raw device pointer to {grid}'s cells; the grid is trusted to already be the right
    // shape and layout; a routine's own {m}/{n}/{lda}/{incx}/... arguments are what tell the
    // library how to read that memory, exactly as they would a raw pointer, so nothing here
    // second-guesses them. the one check worth making on this side is the cell type, since
    // reading a {float32} grid as {float64} is silent corruption rather than a library error
    inline auto data(grid::AnyGrid & grid, char expected, const char * routine) -> void *
    {
        // ask the grid to describe itself
        auto info = grid.view();
        // its cells must match the precision {routine} is named for
        if (info.format.size() != 1 || info.format[0] != expected) {
            // otherwise the caller has reached for the wrong precision-specific routine
            throw py::value_error(
                string_t(routine) + ": expected a grid of cell type '" + expected
                + "', got '" + info.format + "'");
        }
        // hand back the pointer
        return info.ptr;
    }

} // namespace pyre::py::cuda


// end of file
