// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2023 all rights reserved
//

// support
#include <cassert>
// get the tensor algebra
#include <pyre/tensor.h>


// use namespace for readability
using namespace pyre::tensor;


// main program
int main(int argc, char* argv[]) {

    // Packing-independent base for 2D matrix 
    constexpr auto e_00 = matrix_t<2>::unit<0, 0>;
    constexpr auto e_01 = matrix_t<2>::unit<0, 1>;
    constexpr auto e_10 = matrix_t<2>::unit<1, 0>;
    constexpr auto e_11 = matrix_t<2>::unit<1, 1>;
    constexpr auto e_01s = symmetric(matrix_t<2>::unit<0, 1> 
                                            + matrix_t<2>::unit<1, 0>);

    // a 2D matrix
    constexpr auto A = true * e_00 + 2.0 * e_01 + 3.0 * e_10 + 4 * e_11;

    // a 2D symmetric matrix
    constexpr auto B = 1.0 * e_00 + 2.0 * e_01s + 4.0 * e_11;

    // a 2D diagonal matrix
    constexpr auto C = 1.0 * e_00 + 2.0 * e_11;

    // check the math
    static_assert(A + B + C == 3.0 * e_00 + 4.0 * e_01 + 5.0 * e_10 + 10.0 * e_11);
    static_assert(B + C + A == A + B + C);
    static_assert(C + A + B == A + B + C);

    // all done
    return 0;
}


// end of file
