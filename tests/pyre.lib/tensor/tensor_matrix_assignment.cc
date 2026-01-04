// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2026 all rights reserved
//


// support
#include <cassert>
// get the tensor algebra
#include <pyre/tensor.h>


// use namespace for readability
using namespace pyre::tensor;


// main program
int
main(int argc, char * argv[])
{
    // the packing-agnostic canonical basis of R^2x2
    constexpr auto e00 = unit<matrix_t<2>, 0, 0>;
    constexpr auto e01 = unit<matrix_t<2>, 0, 1>;
    constexpr auto e10 = unit<matrix_t<2>, 1, 0>;
    constexpr auto e11 = unit<matrix_t<2>, 1, 1>;
    // the out-of-diagonal basis element for symmetric matrices
    constexpr auto e01_sym = unit<symmetric_matrix_t<2>, 0, 1>;

    // build a canonical matrix
    constexpr auto A_canonical = 1.0 * e00 - 1.0 * e01 - 1.0 * e10 + 2.0 * e11;

    // build a symmetric matrix
    constexpr auto A_symmetric = 1.0 * e00 - 1.0 * e01_sym + 2.0 * e11;

    // build a diagonal matrix
    constexpr auto A_diagonal = 1.0 * e00 + 2.0 * e11;

    // assign a canonical matrix to a canonical matrix
    constexpr matrix_t<2> B_canonical = A_canonical;

    // verify that the assignment worked
    static_assert(B_canonical == A_canonical);

    // assign a symmetric matrix to a symmetric matrix
    constexpr symmetric_matrix_t<2> B_symmetric = A_symmetric;

    // verify that the assignment worked
    static_assert(B_symmetric == A_symmetric);

    // assign a diagonal matrix to a diagonal matrix
    constexpr diagonal_matrix_t<2> B_diagonal = A_diagonal;

    // verify that the assignment worked
    static_assert(B_diagonal == A_diagonal);

    // assign a symmetric matrix to a canonical matrix
    constexpr matrix_t<2> B_canonical_1 = A_symmetric;

    // verify that the assignment worked
    static_assert(B_canonical_1 == A_symmetric);

    // assign a diagonal matrix to a canonical matrix
    constexpr matrix_t<2> B_canonical_2 = A_diagonal;

    // verify that the assignment worked
    static_assert(B_canonical_2 == A_diagonal);

    // assign a canonical matrix to a symmetric matrix (illegal, compiler error)
    // constexpr symmetric_matrix_t<2> C_symmetric = A_canonical;

    // assign a diagonal matrix to a symmetric matrix
    constexpr symmetric_matrix_t<2> C_symmetric = A_diagonal;

    // verify that the assignment worked
    static_assert(C_symmetric == A_diagonal);

    // assign a canonical matrix to a diagonal matrix (illegal, compiler error)
    // constexpr diagonal_matrix_t<2> D_diagonal = A_canonical;

    // assign a symmetric matrix to a diagonal matrix (illegal, compiler error)
    // constexpr diagonal_matrix_t<2> D_diagonal = A_symmetric;

    // all done
    return 0;
}


// end of file
