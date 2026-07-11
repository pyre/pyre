// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"
// the blas
#include <gsl/gsl_blas.h>


// the blas operands' orientation is spelled by the {Transpose}, {Triangle}, {Diagonal}, and
// {Side} enumerations, whose values are gsl's own; so the flags pass straight into the library,
// and a bad flag is unspellable rather than a runtime complaint


// add the bindings for the gsl blas
void
gsl::py::blas(py::module & m)
{
    // level 1: vector-vector operations
    // the scalar product {x^T y}
    m.def(
        // the name
        "blas_ddot",
        // the implementation
        [](const gsl_vector & x, const gsl_vector & y) -> double {
            // room for the answer
            double result = 0;
            // compute it
            gsl_blas_ddot(&x, &y, &result);
            // and hand it back
            return result;
        },
        // the signature
        "x"_a, "y"_a,
        // the docstring
        "the scalar product of {x} and {y}");

    // the euclidean norm of {x}
    m.def(
        // the name
        "blas_dnrm2",
        // the implementation
        [](const gsl_vector & x) -> double { return gsl_blas_dnrm2(&x); },
        // the signature
        "x"_a,
        // the docstring
        "the euclidean norm of {x}");

    // the sum of the absolute values of the entries of {x}
    m.def(
        // the name
        "blas_dasum",
        // the implementation
        [](const gsl_vector & x) -> double { return gsl_blas_dasum(&x); },
        // the signature
        "x"_a,
        // the docstring
        "the sum of the absolute values of the entries of {x}");

    // the index of the entry of {x} with the largest absolute value
    m.def(
        // the name
        "blas_idamax",
        // the implementation
        [](const gsl_vector & x) -> std::size_t { return gsl_blas_idamax(&x); },
        // the signature
        "x"_a,
        // the docstring
        "the index of the entry of {x} with the largest absolute value");

    // exchange the contents of {x} and {y}
    m.def(
        // the name
        "blas_dswap",
        // the implementation
        [](gsl_vector & x, gsl_vector & y) -> void { gsl_blas_dswap(&x, &y); },
        // the signature
        "x"_a, "y"_a,
        // the docstring
        "exchange the contents of {x} and {y}");

    // copy the elements of {x} into {y}
    m.def(
        // the name
        "blas_dcopy",
        // the implementation
        [](const gsl_vector & x, gsl_vector & y) -> void { gsl_blas_dcopy(&x, &y); },
        // the signature
        "x"_a, "y"_a,
        // the docstring
        "copy the elements of {x} into {y}");

    // compute {alpha x + y}, storing the result in {y}
    m.def(
        // the name
        "blas_daxpy",
        // the implementation
        [](double alpha, const gsl_vector & x, gsl_vector & y) -> void {
            // fold {alpha x} into {y}
            gsl_blas_daxpy(alpha, &x, &y);
        },
        // the signature
        "alpha"_a, "x"_a, "y"_a,
        // the docstring
        "compute {alpha x + y}, storing the result in {y}");

    // scale {x} by {alpha}, in place
    m.def(
        // the name
        "blas_dscal",
        // the implementation
        [](double alpha, gsl_vector & x) -> void { gsl_blas_dscal(alpha, &x); },
        // the signature
        "alpha"_a, "x"_a,
        // the docstring
        "scale {x} by {alpha}, in place");

    // the Givens rotation that zeroes the second of the scalars {x} and {y}
    m.def(
        // the name
        "blas_drotg",
        // the implementation
        [](double x, double y) -> std::tuple<double, double, double, double> {
            // room for the cosine and sine of the rotation
            double c = 0, s = 0;
            // compute the rotation, which also overwrites {x} and {y}
            gsl_blas_drotg(&x, &y, &c, &s);
            // and hand back all four
            return { x, y, c, s };
        },
        // the signature
        "x"_a, "y"_a,
        // the docstring
        "the Givens rotation zeroing the second scalar, as the tuple (r, z, c, s)");

    // apply the Givens rotation {(c, s)} to {x} and {y}
    m.def(
        // the name
        "blas_drot",
        // the implementation
        [](gsl_vector & x, gsl_vector & y, double c, double s) -> void {
            // rotate the two vectors together
            gsl_blas_drot(&x, &y, c, s);
        },
        // the signature
        "x"_a, "y"_a, "c"_a, "s"_a,
        // the docstring
        "apply the Givens rotation {(c, s)} to {x} and {y}");

    // level 2: matrix-vector operations
    // compute {y = alpha op(A) x + beta y}
    m.def(
        // the name
        "blas_dgemv",
        // the implementation
        [](CBLAS_TRANSPOSE_t op, double alpha, const gsl_matrix & A, const gsl_vector & x,
           double beta, gsl_vector & y) -> void {
            // the general matrix-vector product
            gsl_blas_dgemv(op, alpha, &A, &x, beta, &y);
        },
        // the signature
        "transpose"_a, "alpha"_a, "A"_a, "x"_a, "beta"_a, "y"_a,
        // the docstring
        "compute {y = alpha op(A) x + beta y}");

    // compute {x = op(A) x} for a triangular {A}
    m.def(
        // the name
        "blas_dtrmv",
        // the implementation
        [](CBLAS_UPLO_t triangle, CBLAS_TRANSPOSE_t op, CBLAS_DIAG_t unit, const gsl_matrix & A,
           gsl_vector & x) -> void {
            // the triangular matrix-vector product
            gsl_blas_dtrmv(triangle, op, unit, &A, &x);
        },
        // the signature
        "uplo"_a, "transpose"_a, "diag"_a, "A"_a, "x"_a,
        // the docstring
        "compute {x = op(A) x} for the triangular {A}");

    // solve {op(A) x = b} for a triangular {A}, with {b} arriving in {x}
    m.def(
        // the name
        "blas_dtrsv",
        // the implementation
        [](CBLAS_UPLO_t triangle, CBLAS_TRANSPOSE_t op, CBLAS_DIAG_t unit, const gsl_matrix & A,
           gsl_vector & x) -> void {
            // the triangular solve
            gsl_blas_dtrsv(triangle, op, unit, &A, &x);
        },
        // the signature
        "uplo"_a, "transpose"_a, "diag"_a, "A"_a, "x"_a,
        // the docstring
        "compute {x = inv(op(A)) x} for the triangular {A}");

    // compute {y = alpha A x + beta y} for a symmetric {A}
    m.def(
        // the name
        "blas_dsymv",
        // the implementation
        [](CBLAS_UPLO_t triangle, double alpha, const gsl_matrix & A, const gsl_vector & x,
           double beta, gsl_vector & y) -> void {
            // the symmetric matrix-vector product
            gsl_blas_dsymv(triangle, alpha, &A, &x, beta, &y);
        },
        // the signature
        "uplo"_a, "alpha"_a, "A"_a, "x"_a, "beta"_a, "y"_a,
        // the docstring
        "compute {y = alpha A x + beta y} for the symmetric {A}");

    // compute the symmetric rank-1 update {A = alpha x x^T + A}
    m.def(
        // the name
        "blas_dsyr",
        // the implementation
        [](CBLAS_UPLO_t triangle, double alpha, const gsl_vector & x, gsl_matrix & A) -> void {
            // the rank-1 update
            gsl_blas_dsyr(triangle, alpha, &x, &A);
        },
        // the signature
        "uplo"_a, "alpha"_a, "x"_a, "A"_a,
        // the docstring
        "compute the symmetric rank-1 update {A = alpha x x^T + A}");

    // level 3: matrix-matrix operations
    // compute {C = alpha op(A) op(B) + beta C}
    m.def(
        // the name
        "blas_dgemm",
        // the implementation
        [](CBLAS_TRANSPOSE_t opA, CBLAS_TRANSPOSE_t opB, double alpha, const gsl_matrix & A,
           const gsl_matrix & B, double beta, gsl_matrix & C) -> void {
            // the general matrix-matrix product
            gsl_blas_dgemm(opA, opB, alpha, &A, &B, beta, &C);
        },
        // the signature
        "tranA"_a, "tranB"_a, "alpha"_a, "A"_a, "B"_a, "beta"_a, "C"_a,
        // the docstring
        "compute {C = alpha op(A) op(B) + beta C}");

    // compute {C = alpha A B + beta C} or {C = alpha B A + beta C} for a symmetric {A}
    m.def(
        // the name
        "blas_dsymm",
        // the implementation
        [](CBLAS_SIDE_t whichSide, CBLAS_UPLO_t triangle, double alpha, const gsl_matrix & A,
           const gsl_matrix & B, double beta, gsl_matrix & C) -> void {
            // the symmetric matrix-matrix product
            gsl_blas_dsymm(whichSide, triangle, alpha, &A, &B, beta, &C);
        },
        // the signature
        "side"_a, "uplo"_a, "alpha"_a, "A"_a, "B"_a, "beta"_a, "C"_a,
        // the docstring
        "compute {C = alpha A B + beta C} or {C = alpha B A + beta C} for the symmetric {A}");

    // compute {B = alpha op(A) B} or {B = alpha B op(A)} for a triangular {A}
    m.def(
        // the name
        "blas_dtrmm",
        // the implementation
        [](CBLAS_SIDE_t whichSide, CBLAS_UPLO_t triangle, CBLAS_TRANSPOSE_t op, CBLAS_DIAG_t unit,
           double alpha, const gsl_matrix & A, gsl_matrix & B) -> void {
            // the triangular matrix-matrix product
            gsl_blas_dtrmm(whichSide, triangle, op, unit, alpha, &A, &B);
        },
        // the signature
        "sideA"_a, "uplo"_a, "transpose"_a, "diag"_a, "alpha"_a, "A"_a, "B"_a,
        // the docstring
        "compute {B = alpha op(A) B} or {B = alpha B op(A)} for the triangular {A}");

    // all done
    return;
}


// end of file
