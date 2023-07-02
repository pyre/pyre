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
    // a 3D matrix
    constexpr matrix_t<3, 3> A { 1, -2, 0, 0, 1, 2, 0, 1, 1 };

    // Jacobi's theorem
    // (odd dimension skew symmetric matrices are singular)
    static_assert(determinant(skew(A)) == 0.0);

    // symmetric matrices have zero skew part
    static_assert(skew(symmetric(A)) == matrix_t<3, 3>::zero);

    // skew-symmetric matrices have zero symmetric part
    static_assert(symmetric(skew(A)) == matrix_t<3, 3>::zero);

    // the skew part of a skew-symmetric matrix is equal to the skew-symmetric matrix
    static_assert(skew(skew(A)) == skew(A));

    // the symmetric part of a symmetric matrix is equal to the symmetric matrix
    static_assert(symmetric(symmetric(A)) == symmetric(A));

    // all done
    return 0;
}


// end of file
