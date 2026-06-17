// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// externals
#include "external.h"

namespace pyre::gsl::py {

void
linalg(::py::module & m)
{
    // LU decomposition: modifies matrix in place, returns (matrix, permutation, sign)
    m.def(
        "linalg_LU_decomp",
        [](::py::object mat_obj) {
            pyre::gsl::Matrix & mat = mat_obj.cast<pyre::gsl::Matrix &>();
            gsl_permutation * p = gsl_permutation_alloc(mat.ptr->size1);
            int sign;
            gsl_linalg_LU_decomp(mat.ptr, p, &sign);
            return ::py::make_tuple(
                mat_obj,
                std::make_unique<pyre::gsl::Permutation>(p, true),
                sign);
        },
        "matrix"_a,
        "compute the LU decomposition of a matrix in place");

    // LU inversion: returns new matrix holding the inverse
    m.def(
        "linalg_LU_invert",
        [](pyre::gsl::Matrix & mat, pyre::gsl::Permutation & p) {
            gsl_matrix * inv = gsl_matrix_alloc(mat.ptr->size1, mat.ptr->size2);
            gsl_linalg_LU_invert(mat.ptr, p.ptr, inv);
            return std::make_unique<pyre::gsl::Matrix>(inv, true);
        },
        "matrix"_a, "permutation"_a,
        "invert a matrix from its LU decomposition");

    // LU determinant
    m.def(
        "linalg_LU_det",
        [](pyre::gsl::Matrix & mat, int sign) -> double {
            return gsl_linalg_LU_det(mat.ptr, sign);
        },
        "matrix"_a, "sign"_a,
        "compute the determinant of a matrix from its LU decomposition");

    // LU log-determinant
    m.def(
        "linalg_LU_lndet",
        [](pyre::gsl::Matrix & mat) -> double {
            return gsl_linalg_LU_lndet(mat.ptr);
        },
        "matrix"_a,
        "compute the log of the absolute value of the determinant from LU decomposition");

    // Cholesky decomposition (in place)
    m.def(
        "linalg_cholesky_decomp",
        [](pyre::gsl::Matrix & mat) {
            gsl_linalg_cholesky_decomp(mat.ptr);
        },
        "matrix"_a,
        "compute the Cholesky decomposition of a positive-definite matrix in place");
}

} // namespace pyre::gsl::py

// end of file
