// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 2021 all rights reserved
//

// system includes
#include <iostream>
#include <cassert>

// dependencies
#include <pyre/algebra/Tensor.h>
#include <pyre/algebra/tensor_algebra.h>

using namespace pyre::algebra;

// main program
int main(int argc, char* argv[]) {

    // Matrix-vector product // TODO: { {0, 1, 2}, {3, 4, 5}, {6, 7, 8} }
    constexpr matrix_t<3, 3> A = { 1, -2, 0, 0, 1, 2, 0, 1, 1 };
    constexpr vector_t<3> x = { 1, 1, 1 };
    constexpr vector_t<3> y = A * x;
    static_assert(inv(A)*y == x);


    // all done
    return 0;
}


// end of file
