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
    // a matrix
    constexpr matrix_t<3, 3> A { 1, -2, 0, 0, 1, 2, 0, 1, 1 };

    // the matrix transpose
    constexpr auto At = transpose(A);

    // transpose of transpose is the identity operator
    static_assert(transpose(At) == A);

    // transpose preserves trace
    static_assert(trace(At) == trace(A));

    // transpose preserves determinant
    static_assert(determinant(At) == determinant(A));

    // all done
    return 0;
}


// end of file
