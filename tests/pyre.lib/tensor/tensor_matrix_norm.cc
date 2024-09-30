// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2024 all rights reserved
//


// support
#include <cassert>
// get the tensor algebra
#include <pyre/tensor.h>


// use namespace for readability
using namespace pyre::tensor;

// the packing-agnostic canonical basis of R^3x3
constexpr auto e00 = unit<matrix_t<3>, 0, 0>;
constexpr auto e01 = unit<matrix_t<3>, 0, 1>;
constexpr auto e02 = unit<matrix_t<3>, 0, 2>;
constexpr auto e10 = unit<matrix_t<3>, 1, 0>;
constexpr auto e11 = unit<matrix_t<3>, 1, 1>;
constexpr auto e12 = unit<matrix_t<3>, 1, 2>;
constexpr auto e20 = unit<matrix_t<3>, 2, 0>;
constexpr auto e21 = unit<matrix_t<3>, 2, 1>;
constexpr auto e22 = unit<matrix_t<3>, 2, 2>;

// the out-of-diagonal basis element for symmetric matrices
constexpr auto e_01_sym = unit<symmetric_matrix_t<3>, 0, 1>;
constexpr auto e_12_sym = unit<symmetric_matrix_t<3>, 1, 2>;


// main program
int
main(int argc, char * argv[])
{
    // construct a matrix in R^3x3
    constexpr auto A =
        2.0 * e00 - 1.0 * e01 - 1.0 * e10 + 2.0 * e11 + 1.0 * e12 + 1.0 * e21 + 2.0 * e22;

    // check that the norm of {A} is correct
    static_assert(norm(A) == 4);

    // construct {A_sym} as a symmetric matrix by construction
    constexpr auto A_sym = 2.0 * e00 - 1.0 * e_01_sym + 2.0 * e11 + 1.0 * e_12_sym + 2.0 * e22;

    // check that the norm of {A_sym} is correct
    static_assert(norm(A_sym) == 4);

    // all done
    return 0;
}


// end of file
