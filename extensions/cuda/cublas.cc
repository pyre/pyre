// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// forward declarations
#include "forward.h"
// the support shared by the library bindings
#include "support.h"


// the vocabulary of the bindings
namespace {
    // the type-erased grid
    using AnyGrid = pyre::py::grid::AnyGrid;
    // the argument literals
    using namespace pybind11::literals;

    // raise the failure the cublas {status} of {routine} reports
    auto check(cublasStatus_t status, const char * routine) -> void
    {
        // if there is one
        if (status != CUBLAS_STATUS_SUCCESS) {
            // say so, in the words of the library
            throw std::runtime_error(std::string(routine) + ": " + cublasGetStatusString(status));
        }
        // all done
        return;
    }

    // the cublas data type of the cells of {grid}
    auto dataType(AnyGrid & grid) -> cudaDataType_t
    {
        // describe the cells
        const auto info = grid.view();
        // single precision
        if (info.format == "f") {
            // is spelled this way
            return CUDA_R_32F;
        }
        // double precision
        if (info.format == "d") {
            // is spelled this way
            return CUDA_R_64F;
        }
        // everything else is out of reach of {gemmex}
        throw pybind11::type_error("gemmex: unsupported cell type '" + info.format + "'");
    }
} // namespace


// the cublas bindings
auto
pyre::cuda::py::cublas(py::module & m) -> void
{
    // the submodule
    auto cublas = m.def_submodule(
        // the name
        "cublas",
        // the docstring
        "thin bindings for cublas, over grids on managed memory");

    // how a matrix is used
    py::enum_<cublasOperation_t>(cublas, "Operation", "how a blas operand is used")
        // as it is
        .value("N", CUBLAS_OP_N, "use the matrix as it is")
        // transposed
        .value("T", CUBLAS_OP_T, "use the transpose of the matrix")
        // conjugate transposed
        .value("C", CUBLAS_OP_C, "use the conjugate transpose of the matrix");

    // which triangle a routine reads
    py::enum_<cublasFillMode_t>(cublas, "FillMode", "which triangle of a matrix a call reads")
        // the lower one
        .value("LOWER", CUBLAS_FILL_MODE_LOWER, "the lower triangle and the diagonal")
        // the upper one
        .value("UPPER", CUBLAS_FILL_MODE_UPPER, "the upper triangle and the diagonal")
        // all of it
        .value("FULL", CUBLAS_FILL_MODE_FULL, "the entire matrix");

    // which side of a product a matrix sits on
    py::enum_<cublasSideMode_t>(cublas, "SideMode", "which side of a product a matrix sits on")
        // the left
        .value("LEFT", CUBLAS_SIDE_LEFT, "the matrix multiplies from the left")
        // the right
        .value("RIGHT", CUBLAS_SIDE_RIGHT, "the matrix multiplies from the right");

    // whether a triangular matrix has a unit diagonal
    py::enum_<cublasDiagType_t>(
        cublas, "DiagType", "whether a triangular matrix has a unit diagonal")
        // as stored
        .value("NON_UNIT", CUBLAS_DIAG_NON_UNIT, "the diagonal entries are as stored")
        // or ones
        .value("UNIT", CUBLAS_DIAG_UNIT, "the diagonal entries are taken to be one");

    // a handle, bound to the current device
    cublas.def(
        // the name
        "create",
        // the implementation
        []() -> std::uintptr_t {
            // make room for the handle
            cublasHandle_t handle = nullptr;
            // make one
            check(cublasCreate(&handle), "create");
            // and hand it off, as the integer python carries
            return fromHandle(handle);
        },
        // the docstring
        "allocate a cublas handle, bound to the current device");

    // the release of a handle
    cublas.def(
        // the name
        "destroy",
        // the implementation
        [](std::uintptr_t handle) -> void {
            // release it
            check(cublasDestroy(toHandle<cublasHandle_t>(handle)), "destroy");
            // all done
            return;
        },
        // the signature
        "handle"_a,
        // the docstring
        "release a cublas {handle}");

    // y = alpha x + y, over float64 cells
    cublas.def(
        // the name
        "daxpy",
        // the implementation
        [](std::uintptr_t handle, int n, double alpha, AnyGrid & x, int incx, AnyGrid & y,
           int incy) -> void {
            // combine the vectors
            check(
                cublasDaxpy(
                    toHandle<cublasHandle_t>(handle), n, &alpha,
                    static_cast<const double *>(data(x, 'd', "daxpy")), incx,
                    static_cast<double *>(data(y, 'd', "daxpy")), incy),
                "daxpy");
            // all done
            return;
        },
        // the signature
        "handle"_a, "n"_a, "alpha"_a, "x"_a, "incx"_a, "y"_a, "incy"_a,
        // the docstring
        "y = alpha * x + y, over grids of {float64} cells");

    // y = alpha x + y, over float32 cells
    cublas.def(
        // the name
        "saxpy",
        // the implementation
        [](std::uintptr_t handle, int n, float alpha, AnyGrid & x, int incx, AnyGrid & y,
           int incy) -> void {
            // combine the vectors
            check(
                cublasSaxpy(
                    toHandle<cublasHandle_t>(handle), n, &alpha,
                    static_cast<const float *>(data(x, 'f', "saxpy")), incx,
                    static_cast<float *>(data(y, 'f', "saxpy")), incy),
                "saxpy");
            // all done
            return;
        },
        // the signature
        "handle"_a, "n"_a, "alpha"_a, "x"_a, "incx"_a, "y"_a, "incy"_a,
        // the docstring
        "y = alpha * x + y, over grids of {float32} cells");

    // C = alpha op(A) op(B) + beta C, over float64 cells, column major
    cublas.def(
        // the name
        "dgemm",
        // the implementation
        [](std::uintptr_t handle, cublasOperation_t transa, cublasOperation_t transb, int m, int n,
           int k, double alpha, AnyGrid & A, int lda, AnyGrid & B, int ldb, double beta,
           AnyGrid & C, int ldc) -> void {
            // form the product
            check(
                cublasDgemm(
                    toHandle<cublasHandle_t>(handle), transa, transb, m, n, k, &alpha,
                    static_cast<const double *>(data(A, 'd', "dgemm")), lda,
                    static_cast<const double *>(data(B, 'd', "dgemm")), ldb, &beta,
                    static_cast<double *>(data(C, 'd', "dgemm")), ldc),
                "dgemm");
            // all done
            return;
        },
        // the signature
        "handle"_a, "transa"_a, "transb"_a, "m"_a, "n"_a, "k"_a, "alpha"_a, "A"_a, "lda"_a, "B"_a,
        "ldb"_a, "beta"_a, "C"_a, "ldc"_a,
        // the docstring
        "C = alpha * op(A) * op(B) + beta * C, over grids of {float64} cells");

    // C = alpha op(A) op(B) + beta C, over float32 cells, column major
    cublas.def(
        // the name
        "sgemm",
        // the implementation
        [](std::uintptr_t handle, cublasOperation_t transa, cublasOperation_t transb, int m, int n,
           int k, float alpha, AnyGrid & A, int lda, AnyGrid & B, int ldb, float beta, AnyGrid & C,
           int ldc) -> void {
            // form the product
            check(
                cublasSgemm(
                    toHandle<cublasHandle_t>(handle), transa, transb, m, n, k, &alpha,
                    static_cast<const float *>(data(A, 'f', "sgemm")), lda,
                    static_cast<const float *>(data(B, 'f', "sgemm")), ldb, &beta,
                    static_cast<float *>(data(C, 'f', "sgemm")), ldc),
                "sgemm");
            // all done
            return;
        },
        // the signature
        "handle"_a, "transa"_a, "transb"_a, "m"_a, "n"_a, "k"_a, "alpha"_a, "A"_a, "lda"_a, "B"_a,
        "ldb"_a, "beta"_a, "C"_a, "ldc"_a,
        // the docstring
        "C = alpha * op(A) * op(B) + beta * C, over grids of {float32} cells");

    // C = alpha op(A) B, or alpha B op(A), with {A} triangular, over float64 cells
    cublas.def(
        // the name
        "dtrmm",
        // the implementation
        [](std::uintptr_t handle, cublasSideMode_t side, cublasFillMode_t uplo,
           cublasOperation_t trans, cublasDiagType_t diag, int m, int n, double alpha, AnyGrid & A,
           int lda, AnyGrid & B, int ldb, AnyGrid & C, int ldc) -> void {
            // form the product
            check(
                cublasDtrmm(
                    toHandle<cublasHandle_t>(handle), side, uplo, trans, diag, m, n, &alpha,
                    static_cast<const double *>(data(A, 'd', "dtrmm")), lda,
                    static_cast<const double *>(data(B, 'd', "dtrmm")), ldb,
                    static_cast<double *>(data(C, 'd', "dtrmm")), ldc),
                "dtrmm");
            // all done
            return;
        },
        // the signature
        "handle"_a, "side"_a, "uplo"_a, "trans"_a, "diag"_a, "m"_a, "n"_a, "alpha"_a, "A"_a,
        "lda"_a, "B"_a, "ldb"_a, "C"_a, "ldc"_a,
        // the docstring
        "C = alpha * op(A) * B, or alpha * B * op(A) on the right, with {A} triangular, over grids "
        "of {float64} cells");

    // C = alpha op(A) B, or alpha B op(A), with {A} triangular, over float32 cells
    cublas.def(
        // the name
        "strmm",
        // the implementation
        [](std::uintptr_t handle, cublasSideMode_t side, cublasFillMode_t uplo,
           cublasOperation_t trans, cublasDiagType_t diag, int m, int n, float alpha, AnyGrid & A,
           int lda, AnyGrid & B, int ldb, AnyGrid & C, int ldc) -> void {
            // form the product
            check(
                cublasStrmm(
                    toHandle<cublasHandle_t>(handle), side, uplo, trans, diag, m, n, &alpha,
                    static_cast<const float *>(data(A, 'f', "strmm")), lda,
                    static_cast<const float *>(data(B, 'f', "strmm")), ldb,
                    static_cast<float *>(data(C, 'f', "strmm")), ldc),
                "strmm");
            // all done
            return;
        },
        // the signature
        "handle"_a, "side"_a, "uplo"_a, "trans"_a, "diag"_a, "m"_a, "n"_a, "alpha"_a, "A"_a,
        "lda"_a, "B"_a, "ldb"_a, "C"_a, "ldc"_a,
        // the docstring
        "C = alpha * op(A) * B, or alpha * B * op(A) on the right, with {A} triangular, over grids "
        "of {float32} cells");

    // x = op(A) x, with {A} triangular, over float64 cells
    cublas.def(
        // the name
        "dtrmv",
        // the implementation
        [](std::uintptr_t handle, cublasFillMode_t uplo, cublasOperation_t trans,
           cublasDiagType_t diag, int n, AnyGrid & A, int lda, AnyGrid & x, int incx) -> void {
            // form the product
            check(
                cublasDtrmv(
                    toHandle<cublasHandle_t>(handle), uplo, trans, diag, n,
                    static_cast<const double *>(data(A, 'd', "dtrmv")), lda,
                    static_cast<double *>(data(x, 'd', "dtrmv")), incx),
                "dtrmv");
            // all done
            return;
        },
        // the signature
        "handle"_a, "uplo"_a, "trans"_a, "diag"_a, "n"_a, "A"_a, "lda"_a, "x"_a, "incx"_a,
        // the docstring
        "x = op(A) * x, with {A} triangular, over grids of {float64} cells");

    // x = op(A) x, with {A} triangular, over float32 cells
    cublas.def(
        // the name
        "strmv",
        // the implementation
        [](std::uintptr_t handle, cublasFillMode_t uplo, cublasOperation_t trans,
           cublasDiagType_t diag, int n, AnyGrid & A, int lda, AnyGrid & x, int incx) -> void {
            // form the product
            check(
                cublasStrmv(
                    toHandle<cublasHandle_t>(handle), uplo, trans, diag, n,
                    static_cast<const float *>(data(A, 'f', "strmv")), lda,
                    static_cast<float *>(data(x, 'f', "strmv")), incx),
                "strmv");
            // all done
            return;
        },
        // the signature
        "handle"_a, "uplo"_a, "trans"_a, "diag"_a, "n"_a, "A"_a, "lda"_a, "x"_a, "incx"_a,
        // the docstring
        "x = op(A) * x, with {A} triangular, over grids of {float32} cells");

    // C = alpha A B + beta C, or alpha B A + beta C, with {A} symmetric, over float64 cells
    cublas.def(
        // the name
        "dsymm",
        // the implementation
        [](std::uintptr_t handle, cublasSideMode_t side, cublasFillMode_t uplo, int m, int n,
           double alpha, AnyGrid & A, int lda, AnyGrid & B, int ldb, double beta, AnyGrid & C,
           int ldc) -> void {
            // form the product
            check(
                cublasDsymm(
                    toHandle<cublasHandle_t>(handle), side, uplo, m, n, &alpha,
                    static_cast<const double *>(data(A, 'd', "dsymm")), lda,
                    static_cast<const double *>(data(B, 'd', "dsymm")), ldb, &beta,
                    static_cast<double *>(data(C, 'd', "dsymm")), ldc),
                "dsymm");
            // all done
            return;
        },
        // the signature
        "handle"_a, "side"_a, "uplo"_a, "m"_a, "n"_a, "alpha"_a, "A"_a, "lda"_a, "B"_a, "ldb"_a,
        "beta"_a, "C"_a, "ldc"_a,
        // the docstring
        "C = alpha * A * B + beta * C, or alpha * B * A + beta * C on the right, with {A} "
        "symmetric, over grids of {float64} cells");

    // C = alpha A B + beta C, or alpha B A + beta C, with {A} symmetric, over float32 cells
    cublas.def(
        // the name
        "ssymm",
        // the implementation
        [](std::uintptr_t handle, cublasSideMode_t side, cublasFillMode_t uplo, int m, int n,
           float alpha, AnyGrid & A, int lda, AnyGrid & B, int ldb, float beta, AnyGrid & C,
           int ldc) -> void {
            // form the product
            check(
                cublasSsymm(
                    toHandle<cublasHandle_t>(handle), side, uplo, m, n, &alpha,
                    static_cast<const float *>(data(A, 'f', "ssymm")), lda,
                    static_cast<const float *>(data(B, 'f', "ssymm")), ldb, &beta,
                    static_cast<float *>(data(C, 'f', "ssymm")), ldc),
                "ssymm");
            // all done
            return;
        },
        // the signature
        "handle"_a, "side"_a, "uplo"_a, "m"_a, "n"_a, "alpha"_a, "A"_a, "lda"_a, "B"_a, "ldb"_a,
        "beta"_a, "C"_a, "ldc"_a,
        // the docstring
        "C = alpha * A * B + beta * C, or alpha * B * A + beta * C on the right, with {A} "
        "symmetric, over grids of {float32} cells");

    // C = alpha op(A) op(B) + beta C, over cells of either precision
    cublas.def(
        // the name
        "gemmex",
        // the implementation
        [](std::uintptr_t handle, cublasOperation_t transa, cublasOperation_t transb, int m, int n,
           int k, double alpha, AnyGrid & A, int lda, AnyGrid & B, int ldb, double beta,
           AnyGrid & C, int ldc) -> void {
            // the type of the cells of each operand
            const auto typeA = dataType(A);
            const auto typeB = dataType(B);
            const auto typeC = dataType(C);
            // the precision of the accumulation follows the result
            const auto compute = typeC == CUDA_R_64F ? CUBLAS_COMPUTE_64F : CUBLAS_COMPUTE_32F;
            // the scalars, in single precision, for single precision accumulation
            const float falpha = static_cast<float>(alpha);
            const float fbeta = static_cast<float>(beta);
            // the scalars in the precision of the accumulation
            const void * palpha = compute == CUBLAS_COMPUTE_64F ?
                                      static_cast<const void *>(&alpha) :
                                      static_cast<const void *>(&falpha);
            const void * pbeta = compute == CUBLAS_COMPUTE_64F ? static_cast<const void *>(&beta) :
                                                                 static_cast<const void *>(&fbeta);
            // form the product
            check(
                cublasGemmEx(
                    toHandle<cublasHandle_t>(handle), transa, transb, m, n, k, palpha,
                    data(A, typeA == CUDA_R_64F ? 'd' : 'f', "gemmex"), typeA, lda,
                    data(B, typeB == CUDA_R_64F ? 'd' : 'f', "gemmex"), typeB, ldb, pbeta,
                    data(C, typeC == CUDA_R_64F ? 'd' : 'f', "gemmex"), typeC, ldc, compute,
                    CUBLAS_GEMM_DEFAULT),
                "gemmex");
            // all done
            return;
        },
        // the signature
        "handle"_a, "transa"_a, "transb"_a, "m"_a, "n"_a, "k"_a, "alpha"_a, "A"_a, "lda"_a, "B"_a,
        "ldb"_a, "beta"_a, "C"_a, "ldc"_a,
        // the docstring
        "C = alpha * op(A) * op(B) + beta * C, over grids of {float32} or {float64} cells");

    // all done
    return;
}


// end of file
