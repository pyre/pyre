// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// externals
#include "external.h"

namespace pyre::gsl::py {

void
blas(::py::module & m)
{
    // -- level 1 ------------------------------------------------------------------

    // dot product of two vectors
    m.def(
        "blas_ddot",
        [](pyre::gsl::Vector & v1, pyre::gsl::Vector & v2) -> double {
            double result;
            gsl_blas_ddot(v1.ptr, v2.ptr, &result);
            return result;
        },
        "v1"_a, "v2"_a,
        "compute the scalar product of two vectors");

    // Euclidean norm of a vector
    m.def(
        "blas_dnrm2",
        [](pyre::gsl::Vector & v) -> double {
            return gsl_blas_dnrm2(v.ptr);
        },
        "v"_a,
        "compute the Euclidean norm of a vector");

    // sum of absolute values of vector entries
    m.def(
        "blas_dasum",
        [](pyre::gsl::Vector & v) -> double {
            return gsl_blas_dasum(v.ptr);
        },
        "v"_a,
        "compute the sum of the absolute values of the vector entries");

    // index of the largest element
    m.def(
        "blas_idamax",
        [](pyre::gsl::Vector & v) -> size_t {
            return static_cast<size_t>(gsl_blas_idamax(v.ptr));
        },
        "v"_a,
        "find the index of the largest element in a vector");

    // swap two vectors
    m.def(
        "blas_dswap",
        [](pyre::gsl::Vector & v1, pyre::gsl::Vector & v2) {
            gsl_blas_dswap(v1.ptr, v2.ptr);
        },
        "v1"_a, "v2"_a,
        "swap the contents of two vectors");

    // copy src into dst
    m.def(
        "blas_dcopy",
        [](pyre::gsl::Vector & src, pyre::gsl::Vector & dst) {
            gsl_blas_dcopy(src.ptr, dst.ptr);
        },
        "src"_a, "dst"_a,
        "copy the contents of one vector into another");

    // y = alpha * x + y
    m.def(
        "blas_daxpy",
        [](double alpha, pyre::gsl::Vector & x, pyre::gsl::Vector & y) {
            gsl_blas_daxpy(alpha, x.ptr, y.ptr);
        },
        "alpha"_a, "x"_a, "y"_a,
        "compute y = alpha * x + y");

    // scale a vector
    m.def(
        "blas_dscal",
        [](double alpha, pyre::gsl::Vector & v) {
            gsl_blas_dscal(alpha, v.ptr);
        },
        "alpha"_a, "v"_a,
        "scale a vector by a scalar");

    // compute Givens rotation parameters
    m.def(
        "blas_drotg",
        [](double a, double b) {
            double c, s;
            gsl_blas_drotg(&a, &b, &c, &s);
            return ::py::make_tuple(a, b, c, s);
        },
        "a"_a, "b"_a,
        "compute the Givens rotation parameters, returning (a, b, c, s)");

    // apply a Givens rotation to two vectors
    m.def(
        "blas_drot",
        [](pyre::gsl::Vector & v1, pyre::gsl::Vector & v2, double c, double s) {
            gsl_blas_drot(v1.ptr, v2.ptr, c, s);
        },
        "v1"_a, "v2"_a, "c"_a, "s"_a,
        "apply a Givens rotation to two vectors");

    // -- level 2 ------------------------------------------------------------------

    // y = alpha * op(A) * x + beta * y
    m.def(
        "blas_dgemv",
        [](int TransA, double alpha, pyre::gsl::Matrix & A, pyre::gsl::Vector & x, double beta,
           pyre::gsl::Vector & y) {
            CBLAS_TRANSPOSE_t trans = (TransA == 0) ? CblasNoTrans
                                    : (TransA == 1) ? CblasTrans
                                                    : CblasConjTrans;
            gsl_blas_dgemv(trans, alpha, A.ptr, x.ptr, beta, y.ptr);
        },
        "TransA"_a, "alpha"_a, "A"_a, "x"_a, "beta"_a, "y"_a,
        "compute y = alpha * op(A) * x + beta * y");

    // x = op(A) * x  (triangular matrix-vector multiply)
    m.def(
        "blas_dtrmv",
        [](int Uplo, int TransA, int Diag, pyre::gsl::Matrix & A, pyre::gsl::Vector & x) {
            CBLAS_UPLO_t uplo = (Uplo == 1) ? CblasUpper : CblasLower;
            CBLAS_TRANSPOSE_t trans = (TransA == 0) ? CblasNoTrans
                                     : (TransA == 1) ? CblasTrans
                                                     : CblasConjTrans;
            CBLAS_DIAG_t diag = (Diag == 0) ? CblasNonUnit : CblasUnit;
            gsl_blas_dtrmv(uplo, trans, diag, A.ptr, x.ptr);
        },
        "Uplo"_a, "TransA"_a, "Diag"_a, "A"_a, "x"_a,
        "compute x = op(A) * x for triangular A");

    // x = inv(op(A)) * x  (triangular solve)
    m.def(
        "blas_dtrsv",
        [](int Uplo, int TransA, int Diag, pyre::gsl::Matrix & A, pyre::gsl::Vector & x) {
            CBLAS_UPLO_t uplo = (Uplo == 1) ? CblasUpper : CblasLower;
            CBLAS_TRANSPOSE_t trans = (TransA == 0) ? CblasNoTrans
                                     : (TransA == 1) ? CblasTrans
                                                     : CblasConjTrans;
            CBLAS_DIAG_t diag = (Diag == 0) ? CblasNonUnit : CblasUnit;
            gsl_blas_dtrsv(uplo, trans, diag, A.ptr, x.ptr);
        },
        "Uplo"_a, "TransA"_a, "Diag"_a, "A"_a, "x"_a,
        "compute x = inv(op(A)) * x for triangular A");

    // y = alpha * A * x + beta * y  (symmetric A)
    m.def(
        "blas_dsymv",
        [](int Uplo, double alpha, pyre::gsl::Matrix & A, pyre::gsl::Vector & x, double beta,
           pyre::gsl::Vector & y) {
            CBLAS_UPLO_t uplo = (Uplo == 1) ? CblasUpper : CblasLower;
            gsl_blas_dsymv(uplo, alpha, A.ptr, x.ptr, beta, y.ptr);
        },
        "Uplo"_a, "alpha"_a, "A"_a, "x"_a, "beta"_a, "y"_a,
        "compute y = alpha * A * x + beta * y for symmetric A");

    // A = alpha * x * x^T + A  (symmetric rank-1 update)
    m.def(
        "blas_dsyr",
        [](int Uplo, double alpha, pyre::gsl::Vector & x, pyre::gsl::Matrix & A) {
            CBLAS_UPLO_t uplo = (Uplo == 1) ? CblasUpper : CblasLower;
            gsl_blas_dsyr(uplo, alpha, x.ptr, A.ptr);
        },
        "Uplo"_a, "alpha"_a, "x"_a, "A"_a,
        "compute A = alpha * x * x^T + A");

    // -- level 3 ------------------------------------------------------------------

    // C = alpha * op(A) * op(B) + beta * C
    m.def(
        "blas_dgemm",
        [](int TransA, int TransB, double alpha, pyre::gsl::Matrix & A, pyre::gsl::Matrix & B, double beta,
           pyre::gsl::Matrix & C) {
            CBLAS_TRANSPOSE_t transA = (TransA == 0) ? CblasNoTrans
                                      : (TransA == 1) ? CblasTrans
                                                      : CblasConjTrans;
            CBLAS_TRANSPOSE_t transB = (TransB == 0) ? CblasNoTrans
                                      : (TransB == 1) ? CblasTrans
                                                      : CblasConjTrans;
            gsl_blas_dgemm(transA, transB, alpha, A.ptr, B.ptr, beta, C.ptr);
        },
        "TransA"_a, "TransB"_a, "alpha"_a, "A"_a, "B"_a, "beta"_a, "C"_a,
        "compute C = alpha * op(A) * op(B) + beta * C");

    // C = alpha * A * B + beta * C  (A symmetric)
    m.def(
        "blas_dsymm",
        [](int Side, int Uplo, double alpha, pyre::gsl::Matrix & A, pyre::gsl::Matrix & B, double beta,
           pyre::gsl::Matrix & C) {
            CBLAS_SIDE_t side = (Side == 0) ? CblasLeft : CblasRight;
            CBLAS_UPLO_t uplo = (Uplo == 1) ? CblasUpper : CblasLower;
            gsl_blas_dsymm(side, uplo, alpha, A.ptr, B.ptr, beta, C.ptr);
        },
        "Side"_a, "Uplo"_a, "alpha"_a, "A"_a, "B"_a, "beta"_a, "C"_a,
        "compute C = alpha * A * B + beta * C where A is symmetric");

    // B = alpha * op(A) * B  (A triangular)
    m.def(
        "blas_dtrmm",
        [](int Side, int Uplo, int TransA, int Diag, double alpha, pyre::gsl::Matrix & A,
           pyre::gsl::Matrix & B) {
            CBLAS_SIDE_t side = (Side == 0) ? CblasLeft : CblasRight;
            CBLAS_UPLO_t uplo = (Uplo == 1) ? CblasUpper : CblasLower;
            CBLAS_TRANSPOSE_t trans = (TransA == 0) ? CblasNoTrans
                                     : (TransA == 1) ? CblasTrans
                                                     : CblasConjTrans;
            CBLAS_DIAG_t diag = (Diag == 0) ? CblasNonUnit : CblasUnit;
            gsl_blas_dtrmm(side, uplo, trans, diag, alpha, A.ptr, B.ptr);
        },
        "Side"_a, "Uplo"_a, "TransA"_a, "Diag"_a, "alpha"_a, "A"_a, "B"_a,
        "compute B = alpha * op(A) * B for triangular A");
}

} // namespace pyre::gsl::py

// end of file
