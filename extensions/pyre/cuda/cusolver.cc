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
// shared handle/pointer support
#include "support.h"


// local support, not part of the public interface
namespace pyre::py {
    namespace {
        // translate a cusolver status into a python exception; cusolver, unlike cublas, has
        // no string translator of its own, so the status code travels in the message as a
        // number
        inline auto
        checkStatus(cusolverStatus_t status, const char * routine) -> void
        {
            if (status == CUSOLVER_STATUS_SUCCESS) {
                return;
            }
            throw std::runtime_error(
                std::string(routine) + ": cusolver error "
                + std::to_string(static_cast<int>(status)));
        }

        // read the factorization outcome cusolver left in {devInfo} back on the host: 0 is
        // success, a positive value names the leading minor that failed to be positive
        // definite, a negative value names an illegal argument; managed memory is
        // host-visible once the device has caught up, so a sync is all reading it back takes
        inline auto
        checkInfo(grid::AnyGrid & devInfo, const char * routine) -> void
        {
            cuda::synchronize(routine);
            auto info = devInfo.view();
            if (info.format.size() != 1 || info.format[0] != 'i') {
                throw py::value_error(std::string(routine) + ": devInfo must be an 'int32' grid");
            }
            auto status = *static_cast<const int *>(info.ptr);
            if (status == 0) {
                return;
            }
            if (status > 0) {
                throw std::runtime_error(
                    std::string(routine) + ": the leading minor of order "
                    + std::to_string(status) + " is not positive definite");
            }
            throw std::runtime_error(
                std::string(routine) + ": argument " + std::to_string(-status)
                + " had an illegal value");
        }
    } // namespace
} // namespace pyre::py


// build the {cusolver} submodule
auto
pyre::py::cuda::cusolver::__init__(py::module & m) -> void
{
    // make the submodule
    auto cusolver = m.def_submodule("cusolver", "thin bindings for cusolverDn");

    // handle lifetime, same convention as {cublas}
    cusolver.def(
        "create",
        []() -> std::uintptr_t {
            cusolverDnHandle_t handle = nullptr;
            checkStatus(cusolverDnCreate(&handle), "create");
            return fromHandle(handle);
        },
        "allocate a cusolverDn handle bound to the current device");

    cusolver.def(
        "destroy",
        [](std::uintptr_t handle) -> void {
            checkStatus(cusolverDnDestroy(toHandle<cusolverDnHandle_t>(handle)), "destroy");
        },
        "handle"_a,
        "release a cusolverDn handle");

    // the cholesky factorization of a symmetric positive definite matrix, in place: on return,
    // the requested triangle of {A} holds the factor
    cusolver.def(
        "dpotrf_buffer_size",
        [](std::uintptr_t handle, cublasFillMode_t uplo, int n, grid::AnyGrid & A, int lda) -> int {
            int lwork = 0;
            checkStatus(
                cusolverDnDpotrf_bufferSize(
                    toHandle<cusolverDnHandle_t>(handle), uplo, n,
                    static_cast<double *>(data(A, 'd', "dpotrf_buffer_size")), lda, &lwork),
                "dpotrf_buffer_size");
            return lwork;
        },
        "handle"_a, "uplo"_a, "n"_a, "A"_a, "lda"_a,
        "the workspace size, in elements, {dpotrf} needs for an n x n {float64} grid");

    cusolver.def(
        "dpotrf",
        [](std::uintptr_t handle, cublasFillMode_t uplo, int n, grid::AnyGrid & A, int lda,
           grid::AnyGrid & workspace, int lwork, grid::AnyGrid & devInfo) -> void {
            checkStatus(
                cusolverDnDpotrf(
                    toHandle<cusolverDnHandle_t>(handle), uplo, n,
                    static_cast<double *>(data(A, 'd', "dpotrf")), lda,
                    static_cast<double *>(data(workspace, 'd', "dpotrf")), lwork,
                    static_cast<int *>(data(devInfo, 'i', "dpotrf"))),
                "dpotrf");
            checkInfo(devInfo, "dpotrf");
        },
        "handle"_a, "uplo"_a, "n"_a, "A"_a, "lda"_a, "workspace"_a, "lwork"_a, "devInfo"_a,
        "factor the {uplo} triangle of the n x n {float64} grid {A} in place, A = L L^T (or "
        "U^T U)");

    // the inverse of a symmetric positive definite matrix from its cholesky factor, in place:
    // {A} must already hold the factor {dpotrf} left behind
    cusolver.def(
        "dpotri_buffer_size",
        [](std::uintptr_t handle, cublasFillMode_t uplo, int n, grid::AnyGrid & A, int lda) -> int {
            int lwork = 0;
            checkStatus(
                cusolverDnDpotri_bufferSize(
                    toHandle<cusolverDnHandle_t>(handle), uplo, n,
                    static_cast<double *>(data(A, 'd', "dpotri_buffer_size")), lda, &lwork),
                "dpotri_buffer_size");
            return lwork;
        },
        "handle"_a, "uplo"_a, "n"_a, "A"_a, "lda"_a,
        "the workspace size, in elements, {dpotri} needs for an n x n {float64} grid");

    cusolver.def(
        "dpotri",
        [](std::uintptr_t handle, cublasFillMode_t uplo, int n, grid::AnyGrid & A, int lda,
           grid::AnyGrid & workspace, int lwork, grid::AnyGrid & devInfo) -> void {
            checkStatus(
                cusolverDnDpotri(
                    toHandle<cusolverDnHandle_t>(handle), uplo, n,
                    static_cast<double *>(data(A, 'd', "dpotri")), lda,
                    static_cast<double *>(data(workspace, 'd', "dpotri")), lwork,
                    static_cast<int *>(data(devInfo, 'i', "dpotri"))),
                "dpotri");
            checkInfo(devInfo, "dpotri");
        },
        "handle"_a, "uplo"_a, "n"_a, "A"_a, "lda"_a, "workspace"_a, "lwork"_a, "devInfo"_a,
        "invert the n x n {float64} grid {A} in place, given its cholesky factor in the "
        "{uplo} triangle; only that triangle of the result is written");
}


// end of file
