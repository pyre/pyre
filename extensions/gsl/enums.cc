// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"
// the blas flag types and the eigenvalue ordering
#include <gsl/gsl_blas.h>
#include <gsl/gsl_eigen.h>


// add the enumerations to the module
//
// these carry gsl's own values, so they pass straight into the library with no translation; the
// blas and eigen bindings take them by these types, which makes an invalid flag impossible to
// spell rather than a runtime complaint
void
gsl::py::enums(py::module & m)
{
    // whether a blas operand is used plain, transposed, or conjugate transposed
    py::enum_<CBLAS_TRANSPOSE_t>(m, "Transpose", "how a blas operand is used")
        .value("noTranspose", CblasNoTrans, "use the matrix as it is")
        .value("transpose", CblasTrans, "use the transpose of the matrix")
        .value("conjugateTranspose", CblasConjTrans, "use the conjugate transpose of the matrix");

    // which triangle of a symmetric or triangular matrix a blas call reads
    py::enum_<CBLAS_UPLO_t>(m, "Triangle", "which triangle of a matrix a blas call reads")
        .value("upper", CblasUpper, "the upper triangle and the diagonal")
        .value("lower", CblasLower, "the lower triangle and the diagonal");

    // whether a triangular matrix has an implicit unit diagonal
    py::enum_<CBLAS_DIAG_t>(m, "Diagonal", "whether a triangular matrix has a unit diagonal")
        .value("unit", CblasUnit, "the diagonal entries are taken to be one")
        .value("nonUnit", CblasNonUnit, "the diagonal entries are as stored");

    // which side of a product a matrix sits on
    py::enum_<CBLAS_SIDE_t>(m, "Side", "which side of a product a matrix sits on")
        .value("left", CblasLeft, "the matrix multiplies from the left")
        .value("right", CblasRight, "the matrix multiplies from the right");

    // the order in which an eigensolver returns its eigenvalues and eigenvectors
    py::enum_<gsl_eigen_sort_t>(m, "EigenOrder", "the ordering of an eigensystem")
        .value("valueAscending", GSL_EIGEN_SORT_VAL_ASC, "by value, smallest first")
        .value("valueDescending", GSL_EIGEN_SORT_VAL_DESC, "by value, largest first")
        .value("magnitudeAscending", GSL_EIGEN_SORT_ABS_ASC, "by magnitude, smallest first")
        .value("magnitudeDescending", GSL_EIGEN_SORT_ABS_DESC, "by magnitude, largest first");

    // all done
    return;
}


// end of file
