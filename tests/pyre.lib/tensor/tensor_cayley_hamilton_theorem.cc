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
int
main(int argc, char * argv[])
{
    // 2D matrix: Cayley-Hamilton's theorem
    // (a matrix is a solution of its characteristic polynomial)
    constexpr matrix_t<2, 2> M { 0, 1, 2, 3 };
    static_assert(
        M * M - trace(M) * M + determinant(M) * matrix_t<2>::identity == matrix_t<2>::zero);

    // 3D matrix: Cayley-Hamilton's theorem
    // (a matrix is a solution of its characteristic polynomial)
    constexpr matrix_t<3, 3> P { 1, -1, -2, 1, 1, 1, -2, 1, 2 };
    static_assert(
        P * P * P - trace(P) * P * P + 0.5 * (trace(P) * trace(P) - trace(P * P)) * P
            - determinant(P) * matrix_t<3>::identity
        == matrix_t<3>::zero);

    // all done
    return 0;
}


// end of file
