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
        // translate a cublas status into a python exception; cublas has carried a string
        // translator since cuda 11.4, so there is no hand-rolled switch to keep in sync
        inline auto
        checkStatus(cublasStatus_t status, const char * routine) -> void
        {
            // the good outcome
            if (status == CUBLAS_STATUS_SUCCESS) {
                return;
            }
            // otherwise, complain, in the caller's own words
            throw std::runtime_error(
                std::string(routine) + ": " + cublasGetStatusString(status));
        }

        // the data type a grid's own cell format names, in cublas's vocabulary; gemmex is the
        // one routine here that reads it, since every other routine is precision-specific by
        // name and simply refuses a mismatched grid
        inline auto
        dataType(const py::buffer_info & info, const char * routine) -> cudaDataType_t
        {
            if (info.format.size() == 1) {
                if (info.format[0] == 'f') {
                    return CUDA_R_32F;
                }
                if (info.format[0] == 'd') {
                    return CUDA_R_64F;
                }
            }
            throw py::value_error(
                std::string(routine) + ": unsupported grid cell type '" + info.format + "'");
        }
    } // namespace
} // namespace pyre::py


// build the {cublas} submodule
auto
pyre::py::cuda::cublas::__init__(py::module & m) -> void
{
    // make the submodule
    auto cublas = m.def_submodule("cublas", "thin bindings for cublas");

    // the operand orientation, fill mode, side, and diagonal flags carry cublas's own values,
    // so they pass straight into the library and a bad flag is unspellable rather than a
    // runtime complaint
    py::enum_<cublasOperation_t>(cublas, "Operation", "how a blas operand is used")
        .value("N", CUBLAS_OP_N, "use the matrix as it is")
        .value("T", CUBLAS_OP_T, "use the transpose of the matrix")
        .value("C", CUBLAS_OP_C, "use the conjugate transpose of the matrix");

    py::enum_<cublasFillMode_t>(cublas, "FillMode", "which triangle of a matrix a call reads")
        .value("LOWER", CUBLAS_FILL_MODE_LOWER, "the lower triangle and the diagonal")
        .value("UPPER", CUBLAS_FILL_MODE_UPPER, "the upper triangle and the diagonal")
        .value("FULL", CUBLAS_FILL_MODE_FULL, "the entire matrix");

    py::enum_<cublasSideMode_t>(cublas, "SideMode", "which side of a product a matrix sits on")
        .value("LEFT", CUBLAS_SIDE_LEFT, "the matrix multiplies from the left")
        .value("RIGHT", CUBLAS_SIDE_RIGHT, "the matrix multiplies from the right");

    py::enum_<cublasDiagType_t>(cublas, "DiagType", "whether a triangular matrix has a unit diagonal")
        .value("NON_UNIT", CUBLAS_DIAG_NON_UNIT, "the diagonal entries are as stored")
        .value("UNIT", CUBLAS_DIAG_UNIT, "the diagonal entries are taken to be one");

    // handle lifetime: a cublas handle binds to whichever device is current when it is
    // created, and every call below takes one explicitly, exactly like nvmath's own low-level
    // bindings -- there is no handle hidden behind these functions
    cublas.def(
        "create",
        []() -> std::uintptr_t {
            cublasHandle_t handle = nullptr;
            checkStatus(cublasCreate(&handle), "create");
            return fromHandle(handle);
        },
        "allocate a cublas handle bound to the current device");

    cublas.def(
        "destroy",
        [](std::uintptr_t handle) -> void {
            checkStatus(cublasDestroy(toHandle<cublasHandle_t>(handle)), "destroy");
        },
        "handle"_a,
        "release a cublas handle");

    // level 1: y = alpha x + y
    cublas.def(
        "daxpy",
        [](std::uintptr_t handle, int n, double alpha, grid::AnyGrid & x, int incx,
           grid::AnyGrid & y, int incy) -> void {
            checkStatus(
                cublasDaxpy(
                    toHandle<cublasHandle_t>(handle), n, &alpha,
                    static_cast<const double *>(data(x, 'd', "daxpy")), incx,
                    static_cast<double *>(data(y, 'd', "daxpy")), incy),
                "daxpy");
            synchronize("daxpy");
        },
        "handle"_a, "n"_a, "alpha"_a, "x"_a, "incx"_a, "y"_a, "incy"_a,
        "y = alpha * x + y, over grids of {float64} cells");

    // level 3: C = alpha op(A) op(B) + beta C, column major, exactly as cublas itself reads it
    cublas.def(
        "dgemm",
        [](std::uintptr_t handle, cublasOperation_t transa, cublasOperation_t transb, int m,
           int n, int k, double alpha, grid::AnyGrid & A, int lda, grid::AnyGrid & B, int ldb,
           double beta, grid::AnyGrid & C, int ldc) -> void {
            checkStatus(
                cublasDgemm(
                    toHandle<cublasHandle_t>(handle), transa, transb, m, n, k, &alpha,
                    static_cast<const double *>(data(A, 'd', "dgemm")), lda,
                    static_cast<const double *>(data(B, 'd', "dgemm")), ldb, &beta,
                    static_cast<double *>(data(C, 'd', "dgemm")), ldc),
                "dgemm");
            synchronize("dgemm");
        },
        "handle"_a, "transa"_a, "transb"_a, "m"_a, "n"_a, "k"_a, "alpha"_a, "A"_a, "lda"_a,
        "B"_a, "ldb"_a, "beta"_a, "C"_a, "ldc"_a,
        "C = alpha * op(A) * op(B) + beta * C, over grids of {float64} cells, column major");

    // the mixed precision counterpart: {A}, {B}, {C} may each be {float32} or {float64}; the
    // accumulation type follows {C}
    cublas.def(
        "gemmex",
        [](std::uintptr_t handle, cublasOperation_t transa, cublasOperation_t transb, int m,
           int n, int k, double alpha, grid::AnyGrid & A, int lda, grid::AnyGrid & B, int ldb,
           double beta, grid::AnyGrid & C, int ldc) -> void {
            auto infoA = A.view();
            auto infoB = B.view();
            auto infoC = C.view();
            auto typeA = dataType(infoA, "gemmex");
            auto typeB = dataType(infoB, "gemmex");
            auto typeC = dataType(infoC, "gemmex");
            // the accumulation precision tracks the output
            auto compute =
                (typeC == CUDA_R_64F) ? CUBLAS_COMPUTE_64F : CUBLAS_COMPUTE_32F;
            // alpha/beta are read at the accumulation precision
            float falpha = static_cast<float>(alpha), fbeta = static_cast<float>(beta);
            const void * palpha = (compute == CUBLAS_COMPUTE_64F)
                ? static_cast<const void *>(&alpha)
                : static_cast<const void *>(&falpha);
            const void * pbeta = (compute == CUBLAS_COMPUTE_64F)
                ? static_cast<const void *>(&beta)
                : static_cast<const void *>(&fbeta);
            checkStatus(
                cublasGemmEx(
                    toHandle<cublasHandle_t>(handle), transa, transb, m, n, k, palpha,
                    infoA.ptr, typeA, lda, infoB.ptr, typeB, ldb, pbeta, infoC.ptr, typeC, ldc,
                    compute, CUBLAS_GEMM_DEFAULT),
                "gemmex");
            synchronize("gemmex");
        },
        "handle"_a, "transa"_a, "transb"_a, "m"_a, "n"_a, "k"_a, "alpha"_a, "A"_a, "lda"_a,
        "B"_a, "ldb"_a, "beta"_a, "C"_a, "ldc"_a,
        "C = alpha * op(A) * op(B) + beta * C, {A}/{B}/{C} each {float32} or {float64}");

    // triangular matrix-matrix product: C = alpha op(A) B (side left) or alpha B op(A) (side
    // right), {A} triangular, out of place
    cublas.def(
        "dtrmm",
        [](std::uintptr_t handle, cublasSideMode_t side, cublasFillMode_t uplo,
           cublasOperation_t trans, cublasDiagType_t diag, int m, int n, double alpha,
           grid::AnyGrid & A, int lda, grid::AnyGrid & B, int ldb, grid::AnyGrid & C,
           int ldc) -> void {
            checkStatus(
                cublasDtrmm(
                    toHandle<cublasHandle_t>(handle), side, uplo, trans, diag, m, n, &alpha,
                    static_cast<const double *>(data(A, 'd', "dtrmm")), lda,
                    static_cast<const double *>(data(B, 'd', "dtrmm")), ldb,
                    static_cast<double *>(data(C, 'd', "dtrmm")), ldc),
                "dtrmm");
            synchronize("dtrmm");
        },
        "handle"_a, "side"_a, "uplo"_a, "trans"_a, "diag"_a, "m"_a, "n"_a, "alpha"_a, "A"_a,
        "lda"_a, "B"_a, "ldb"_a, "C"_a, "ldc"_a,
        "C = alpha * op(A) * B (or B * op(A) on the right), {A} triangular, {float64} cells");

    // triangular matrix-vector product, in place: x = op(A) x
    cublas.def(
        "dtrmv",
        [](std::uintptr_t handle, cublasFillMode_t uplo, cublasOperation_t trans,
           cublasDiagType_t diag, int n, grid::AnyGrid & A, int lda, grid::AnyGrid & x,
           int incx) -> void {
            checkStatus(
                cublasDtrmv(
                    toHandle<cublasHandle_t>(handle), uplo, trans, diag, n,
                    static_cast<const double *>(data(A, 'd', "dtrmv")), lda,
                    static_cast<double *>(data(x, 'd', "dtrmv")), incx),
                "dtrmv");
            synchronize("dtrmv");
        },
        "handle"_a, "uplo"_a, "trans"_a, "diag"_a, "n"_a, "A"_a, "lda"_a, "x"_a, "incx"_a,
        "x = op(A) * x, {A} triangular n x n, {float64} cells");

    // symmetric matrix-matrix product: C = alpha A B + beta C (side left) or alpha B A + beta
    // C (side right), {A} symmetric
    cublas.def(
        "dsymm",
        [](std::uintptr_t handle, cublasSideMode_t side, cublasFillMode_t uplo, int m, int n,
           double alpha, grid::AnyGrid & A, int lda, grid::AnyGrid & B, int ldb, double beta,
           grid::AnyGrid & C, int ldc) -> void {
            checkStatus(
                cublasDsymm(
                    toHandle<cublasHandle_t>(handle), side, uplo, m, n, &alpha,
                    static_cast<const double *>(data(A, 'd', "dsymm")), lda,
                    static_cast<const double *>(data(B, 'd', "dsymm")), ldb, &beta,
                    static_cast<double *>(data(C, 'd', "dsymm")), ldc),
                "dsymm");
            synchronize("dsymm");
        },
        "handle"_a, "side"_a, "uplo"_a, "m"_a, "n"_a, "alpha"_a, "A"_a, "lda"_a, "B"_a, "ldb"_a,
        "beta"_a, "C"_a, "ldc"_a,
        "C = alpha * A * B + beta * C (or alpha * B * A on the right), {A} symmetric, "
        "{float64} cells");
}


// end of file
