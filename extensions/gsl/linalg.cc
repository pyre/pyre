// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"
// the linear algebra, and the permutations its decompositions produce
#include <gsl/gsl_linalg.h>
#include <gsl/gsl_permutation.h>


// add the bindings for the gsl linear algebra
void
gsl::py::linalg(py::module & m)
{
    // the LU decomposition
    //
    // gsl works in place, overwriting {matrix} with its own L and U factors and filling
    // {permutation} with the row interchanges; the caller allocates both, and we hand back the
    // sign of the permutation, which the determinant needs
    m.def(
        // the name
        "linalg_LU_decomp",
        // the implementation
        [](gsl_matrix & matrix, gsl_permutation & permutation) -> int {
            // room for the sign of the permutation
            int sign = 0;
            // decompose, in place
            gsl_linalg_LU_decomp(&matrix, &permutation, &sign);
            // and report the sign
            return sign;
        },
        // the signature
        "matrix"_a, "permutation"_a,
        // the docstring
        "replace {matrix} with its LU decomposition, fill {permutation}, and return the sign");

    // the inverse, from an LU decomposition
    //
    // {matrix} and {permutation} are the output of {LU_decomp}; the caller allocates {inverse}
    // to the shape of the original matrix, and we fill it
    m.def(
        // the name
        "linalg_LU_invert",
        // the implementation
        [](const gsl_matrix & matrix, const gsl_permutation & permutation,
           gsl_matrix & inverse) -> void {
            // gsl reads the factors and writes the inverse
            gsl_linalg_LU_invert(&matrix, &permutation, &inverse);
        },
        // the signature
        "matrix"_a, "permutation"_a, "inverse"_a,
        // the docstring
        "fill {inverse} from the LU-decomposed {matrix} and its {permutation}");

    // the determinant, from an LU decomposition
    m.def(
        // the name
        "linalg_LU_det",
        // the implementation
        [](gsl_matrix & matrix, int sign) -> double {
            // gsl multiplies the diagonal, then the sign
            return gsl_linalg_LU_det(&matrix, sign);
        },
        // the signature
        "matrix"_a, "sign"_a,
        // the docstring
        "the determinant of the LU-decomposed {matrix}, given the {sign} of its permutation");

    // the logarithm of the absolute value of the determinant, from an LU decomposition
    m.def(
        // the name
        "linalg_LU_lndet",
        // the implementation
        [](gsl_matrix & matrix) -> double {
            // gsl sums the logs of the diagonal
            return gsl_linalg_LU_lndet(&matrix);
        },
        // the signature
        "matrix"_a,
        // the docstring
        "the log of the absolute determinant of the LU-decomposed {matrix}");

    // the Cholesky decomposition of a symmetric positive definite matrix, in place
    m.def(
        // the name
        "linalg_cholesky_decomp",
        // the implementation
        [](gsl_matrix & matrix) -> void {
            // gsl overwrites {matrix} with its Cholesky factors
            gsl_linalg_cholesky_decomp(&matrix);
        },
        // the signature
        "matrix"_a,
        // the docstring
        "replace the symmetric positive definite {matrix} with its Cholesky decomposition");

    // all done
    return;
}


// end of file
