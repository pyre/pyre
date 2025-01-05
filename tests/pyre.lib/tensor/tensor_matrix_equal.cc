// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2025 all rights reserved
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

    // build a matrix
    constexpr auto A = 1.0 * e00 - 1.0 * e01 - 1.0 * e10 + 2.0 * e11;

    // check that {A} is not a symmetric matrix by construction (it just happens to be symmetric)
    static_assert(A.is_symmetric() == false);

    // build the same matrix but with the symmetric basis
    constexpr auto A_sym = 1.0 * e00 - 1.0 * e01_sym + 2.0 * e11;

    // check that {A_sym} is a symmetric matrix by construction
    static_assert(A_sym.is_symmetric() == true);

    // verify matrix-matrix product
    static_assert(A == A_sym);

    // all done
    return 0;
}


// end of file
