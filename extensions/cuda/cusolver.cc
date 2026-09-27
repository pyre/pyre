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
// the support shared by the library bindings
#include "support.h"


// the vocabulary of the bindings
namespace {
    // the type-erased grid
    using AnyGrid = pyre::py::grid::AnyGrid;
    // the argument literals
    using namespace pybind11::literals;

    // raise the failure the cusolver {status} of {routine} reports
    auto check(cusolverStatus_t status, const char * routine) -> void
    {
        // if there is one
        if (status != CUSOLVER_STATUS_SUCCESS) {
            // say so
            throw std::runtime_error(
                std::string(routine) + ": cusolver error "
                + std::to_string(static_cast<int>(status)));
        }
        // all done
        return;
    }

    // raise the failure {routine} reports in its {devInfo}
    auto checkInfo(AnyGrid & devInfo, const char * routine) -> void
    {
        // the status is written by the device, so wait for it
        pyre::cuda::py::DeviceEngine::access();
        // read it
        const auto status = *static_cast<const int *>(devInfo.view().ptr);
        // a positive status names the leading minor that is not positive definite
        if (status > 0) {
            // so say so
            throw std::runtime_error(
                std::string(routine) + ": the leading minor of order " + std::to_string(status)
                + " is not positive definite");
        }
        // a negative one names the argument with an illegal value
        if (status < 0) {
            // so say so
            throw std::runtime_error(
                std::string(routine) + ": argument " + std::to_string(-status)
                + " has an illegal value");
        }
        // all done
        return;
    }
} // namespace


// the cusolver bindings
auto
pyre::cuda::py::cusolver(py::module & m) -> void
{
    // the submodule
    auto cusolver = m.def_submodule(
        // the name
        "cusolver",
        // the docstring
        "thin bindings for the dense cusolver routines, over grids on managed memory");

    // a handle, bound to the current device
    cusolver.def(
        // the name
        "create",
        // the implementation
        []() -> std::uintptr_t {
            // make room for the handle
            cusolverDnHandle_t handle = nullptr;
            // make one
            check(cusolverDnCreate(&handle), "create");
            // and hand it off, as the integer python carries
            return fromHandle(handle);
        },
        // the docstring
        "allocate a cusolver handle, bound to the current device");

    // the release of a handle
    cusolver.def(
        // the name
        "destroy",
        // the implementation
        [](std::uintptr_t handle) -> void {
            // release it
            check(cusolverDnDestroy(toHandle<cusolverDnHandle_t>(handle)), "destroy");
            // all done
            return;
        },
        // the signature
        "handle"_a,
        // the docstring
        "release a cusolver {handle}");

    // the workspace dpotrf needs, in cells
    cusolver.def(
        // the name
        "dpotrf_buffer_size",
        // the implementation
        [](std::uintptr_t handle, cublasFillMode_t uplo, int n, AnyGrid & A, int lda) -> int {
            // make room for the answer
            int lwork = 0;
            // ask the library
            check(
                cusolverDnDpotrf_bufferSize(
                    toHandle<cusolverDnHandle_t>(handle), uplo, n,
                    static_cast<double *>(data(A, 'd', "dpotrf_buffer_size")), lda, &lwork),
                "dpotrf_buffer_size");
            // hand off the size
            return lwork;
        },
        // the signature
        "handle"_a, "uplo"_a, "n"_a, "A"_a, "lda"_a,
        // the docstring
        "the size of the workspace, in cells, {dpotrf} needs for the n x n {float64} grid {A}");

    // factor a symmetric positive definite matrix of float64 cells in place
    cusolver.def(
        // the name
        "dpotrf",
        // the implementation
        [](std::uintptr_t handle, cublasFillMode_t uplo, int n, AnyGrid & A, int lda,
           AnyGrid & workspace, int lwork, AnyGrid & devInfo) -> void {
            // factor it
            check(
                cusolverDnDpotrf(
                    toHandle<cusolverDnHandle_t>(handle), uplo, n,
                    static_cast<double *>(data(A, 'd', "dpotrf")), lda,
                    static_cast<double *>(data(workspace, 'd', "dpotrf")), lwork,
                    static_cast<int *>(data(devInfo, 'i', "dpotrf"))),
                "dpotrf");
            // and check how it went
            checkInfo(devInfo, "dpotrf");
            // all done
            return;
        },
        // the signature
        "handle"_a, "uplo"_a, "n"_a, "A"_a, "lda"_a, "workspace"_a, "lwork"_a, "devInfo"_a,
        // the docstring
        "factor the {uplo} triangle of the n x n {float64} grid {A} in place, A = L L^T or U^T U; "
        "waits for the device and raises when the factorization fails");

    // the workspace dpotri needs, in cells
    cusolver.def(
        // the name
        "dpotri_buffer_size",
        // the implementation
        [](std::uintptr_t handle, cublasFillMode_t uplo, int n, AnyGrid & A, int lda) -> int {
            // make room for the answer
            int lwork = 0;
            // ask the library
            check(
                cusolverDnDpotri_bufferSize(
                    toHandle<cusolverDnHandle_t>(handle), uplo, n,
                    static_cast<double *>(data(A, 'd', "dpotri_buffer_size")), lda, &lwork),
                "dpotri_buffer_size");
            // hand off the size
            return lwork;
        },
        // the signature
        "handle"_a, "uplo"_a, "n"_a, "A"_a, "lda"_a,
        // the docstring
        "the size of the workspace, in cells, {dpotri} needs for the n x n {float64} grid {A}");

    // invert a symmetric positive definite matrix of float64 cells in place
    cusolver.def(
        // the name
        "dpotri",
        // the implementation
        [](std::uintptr_t handle, cublasFillMode_t uplo, int n, AnyGrid & A, int lda,
           AnyGrid & workspace, int lwork, AnyGrid & devInfo) -> void {
            // invert it
            check(
                cusolverDnDpotri(
                    toHandle<cusolverDnHandle_t>(handle), uplo, n,
                    static_cast<double *>(data(A, 'd', "dpotri")), lda,
                    static_cast<double *>(data(workspace, 'd', "dpotri")), lwork,
                    static_cast<int *>(data(devInfo, 'i', "dpotri"))),
                "dpotri");
            // and check how it went
            checkInfo(devInfo, "dpotri");
            // all done
            return;
        },
        // the signature
        "handle"_a, "uplo"_a, "n"_a, "A"_a, "lda"_a, "workspace"_a, "lwork"_a, "devInfo"_a,
        // the docstring
        "invert the n x n {float64} grid {A} in place, given its cholesky factor in the {uplo} "
        "triangle; waits for the device and raises when the inversion fails");

    // the workspace spotrf needs, in cells
    cusolver.def(
        // the name
        "spotrf_buffer_size",
        // the implementation
        [](std::uintptr_t handle, cublasFillMode_t uplo, int n, AnyGrid & A, int lda) -> int {
            // make room for the answer
            int lwork = 0;
            // ask the library
            check(
                cusolverDnSpotrf_bufferSize(
                    toHandle<cusolverDnHandle_t>(handle), uplo, n,
                    static_cast<float *>(data(A, 'f', "spotrf_buffer_size")), lda, &lwork),
                "spotrf_buffer_size");
            // hand off the size
            return lwork;
        },
        // the signature
        "handle"_a, "uplo"_a, "n"_a, "A"_a, "lda"_a,
        // the docstring
        "the size of the workspace, in cells, {spotrf} needs for the n x n {float32} grid {A}");

    // factor a symmetric positive definite matrix of float32 cells in place
    cusolver.def(
        // the name
        "spotrf",
        // the implementation
        [](std::uintptr_t handle, cublasFillMode_t uplo, int n, AnyGrid & A, int lda,
           AnyGrid & workspace, int lwork, AnyGrid & devInfo) -> void {
            // factor it
            check(
                cusolverDnSpotrf(
                    toHandle<cusolverDnHandle_t>(handle), uplo, n,
                    static_cast<float *>(data(A, 'f', "spotrf")), lda,
                    static_cast<float *>(data(workspace, 'f', "spotrf")), lwork,
                    static_cast<int *>(data(devInfo, 'i', "spotrf"))),
                "spotrf");
            // and check how it went
            checkInfo(devInfo, "spotrf");
            // all done
            return;
        },
        // the signature
        "handle"_a, "uplo"_a, "n"_a, "A"_a, "lda"_a, "workspace"_a, "lwork"_a, "devInfo"_a,
        // the docstring
        "factor the {uplo} triangle of the n x n {float32} grid {A} in place, A = L L^T or U^T U; "
        "waits for the device and raises when the factorization fails");

    // the workspace spotri needs, in cells
    cusolver.def(
        // the name
        "spotri_buffer_size",
        // the implementation
        [](std::uintptr_t handle, cublasFillMode_t uplo, int n, AnyGrid & A, int lda) -> int {
            // make room for the answer
            int lwork = 0;
            // ask the library
            check(
                cusolverDnSpotri_bufferSize(
                    toHandle<cusolverDnHandle_t>(handle), uplo, n,
                    static_cast<float *>(data(A, 'f', "spotri_buffer_size")), lda, &lwork),
                "spotri_buffer_size");
            // hand off the size
            return lwork;
        },
        // the signature
        "handle"_a, "uplo"_a, "n"_a, "A"_a, "lda"_a,
        // the docstring
        "the size of the workspace, in cells, {spotri} needs for the n x n {float32} grid {A}");

    // invert a symmetric positive definite matrix of float32 cells in place
    cusolver.def(
        // the name
        "spotri",
        // the implementation
        [](std::uintptr_t handle, cublasFillMode_t uplo, int n, AnyGrid & A, int lda,
           AnyGrid & workspace, int lwork, AnyGrid & devInfo) -> void {
            // invert it
            check(
                cusolverDnSpotri(
                    toHandle<cusolverDnHandle_t>(handle), uplo, n,
                    static_cast<float *>(data(A, 'f', "spotri")), lda,
                    static_cast<float *>(data(workspace, 'f', "spotri")), lwork,
                    static_cast<int *>(data(devInfo, 'i', "spotri"))),
                "spotri");
            // and check how it went
            checkInfo(devInfo, "spotri");
            // all done
            return;
        },
        // the signature
        "handle"_a, "uplo"_a, "n"_a, "A"_a, "lda"_a, "workspace"_a, "lwork"_a, "devInfo"_a,
        // the docstring
        "invert the n x n {float32} grid {A} in place, given its cholesky factor in the {uplo} "
        "triangle; waits for the device and raises when the inversion fails");

    // all done
    return;
}


// end of file
