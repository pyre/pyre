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
    // two vectors in 3D
    constexpr auto v1 = vector_t<3, int> { -2, 2, 10 };
    constexpr auto v2 = vector_t<3> { 1.0, 2.0, 3.0 / 2.0 };

    // use {v1} and {v2} to build {A_row} row-wise
    constexpr auto A_row = rows(v1, v2);
    // expected result
    constexpr auto A_exp_row = matrix_t<2, 3> { -2.0, 2.0, 10.0, 1.0, 2.0, 3.0 / 2.0 };
    // verify result
    static_assert(A_exp_row == A_row);

    // use {v1} and {v2} to build {A_col} column-wise
    constexpr auto A_col = columns(v1, v2);
    // expected result
    constexpr auto A_exp_col = pyre::tensor::transpose(A_exp_row);
    // verify result
    static_assert(A_exp_col == A_col);

    // all done
    return 0;
}


// end of file
