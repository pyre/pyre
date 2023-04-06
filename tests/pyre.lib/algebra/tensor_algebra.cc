// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 2021 all rights reserved
//


// support
#include <cassert>
// get the tensor algebra
#include <pyre/algebra.h>


// use namespace for readability
using namespace pyre::algebra;


// main program
int main(int argc, char* argv[]) {

    // matrix-vector product and inverse
    constexpr matrix_t<3, 3> A { 1, -2, 0, 0, 1, 2, 0, 1, 1 };
    constexpr vector_t<3> x { 1, 1, 1 };
    constexpr scalar_t a = -2.0;
    constexpr vector_t<3> y = a * A * x;
    static_assert(inverse(A) * y / a == x);

    // matrix-matrix product
    constexpr matrix_t<3, 3> B { 1, 0, 0, 0, 2, 0, 0, 0, 3 };
    constexpr matrix_t<3, 3> B2 { 1, 0, 0, 0, 4, 0, 0, 0, 9 };
    static_assert(B * B == B2);

    // all done
    return 0;
}


// end of file
