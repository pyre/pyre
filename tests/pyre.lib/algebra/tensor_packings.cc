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

// use namespace for readability
using namespace pyre::algebra;

// main program
int main(int argc, char* argv[]) {

    // TOFIX: can we make these independent of the packing? 
    static constexpr auto e00 = diagonal_matrix_t<2>::unit(0, 0);
    static constexpr auto e01 = matrix_t<2, 2>::unit(0, 1);
    static constexpr auto e10 = matrix_t<2, 2>::unit(1, 0);
    static constexpr auto e11 = diagonal_matrix_t<2>::unit(1, 1);
    static constexpr auto e01s = symmetric_matrix_t<2>::unit(0, 1);

    static constexpr matrix_t<2, 2> A = 1.0 * e00 + 2.0 * e01 + 3.0 * e10 + 4.0 * e11;

    static constexpr symmetric_matrix_t<2> B = 1.0 * e00 + 2.0 * e01s + 4.0 * e11;

    static constexpr diagonal_matrix_t<2> C = 1.0 * e00 + 2.0 * e11;

    static_assert(A + B + C == matrix_t<2, 2> {3, 4, 5, 10});
    // static_assert(B + C + A == matrix_t<2, 2> {3, 4, 5, 10}); // TOFIX
    // std::cout << B + C + A << std::endl;
    static_assert(C + A + B == matrix_t<2, 2> {3, 4, 5, 10});

    // all done
    return 0;
}

// end of file
