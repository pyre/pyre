// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 2021 all rights reserved
//

// support
#include <cassert>
// #include <iostream> //TOFIX

// get the tensor algebra
#include <pyre/algebra/tensor_algebra.h>
#include <pyre/algebra/VectorBasis.h>
#include <pyre/algebra/MatrixBasis.h>

// use namespace for readability
using namespace pyre::algebra;

// main program
int main(int argc, char* argv[]) {

    // Packing-independent base for 2D matrix 
    static constexpr auto e_00 = MatrixBasis<2>::unit<0, 0>;
    static constexpr auto e_01 = MatrixBasis<2>::unit<0, 1>;
    static constexpr auto e_10 = MatrixBasis<2>::unit<1, 0>;
    static constexpr auto e_11 = MatrixBasis<2>::unit<1, 1>;
    static constexpr auto e_01s = symmetric(MatrixBasis<2>::unit<0, 1> + MatrixBasis<2>::unit<1, 0>);

    // a 2D matrix
    static constexpr matrix_t<2, 2> A = 1.0 * e_00 + 2.0 * e_01 + 3.0 * e_10 + 4.0 * e_11;

    // a 2D symmetric matrix
    static constexpr symmetric_matrix_t<2> B = 1.0 * e_00 + 2.0 * e_01s + 4.0 * e_11;

    // a 2D diagonal matrix
    static constexpr diagonal_matrix_t<2> C = 1.0 * e_00 + 2.0 * e_11;

    // check the math
    static_assert(A + B + C == matrix_t<2, 2> {3, 4, 5, 10});
    // static_assert(B + C + A == matrix_t<2, 2> {3, 4, 5, 10}); // TOFIX
    // std::cout << B + C + A << std::endl;
    static_assert(C + A + B == matrix_t<2, 2> {3, 4, 5, 10});

    // all done
    return 0;
}

// end of file
