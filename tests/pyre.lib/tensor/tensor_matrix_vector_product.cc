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


// main program
int
main(int argc, char * argv[])
{
    // a 2x1 matrix (aka column vector)
    constexpr auto a1 = matrix_t<2, 1> { 1.0, 1.0 };
    // a 2x2 matrix
    constexpr auto C1 = matrix_t<2, 2> { 2.0, 0.0, 1.0, 2.0 };
    // a quadratic form
    constexpr auto q1 = transpose(a1) * C1 * a1;
    // check that the value is correct
    static_assert(q1 == 5.0);

    // a 2D vector
    constexpr auto a2 = vector_t<2> { 1.0, 1.0 };
    // a 2x2 matrix
    constexpr auto C2 = matrix_t<2, 2> { 2.0, 0.0, 1.0, 2.0 };
    // a quadratic form
    constexpr auto q2 = transpose(a2) * C2 * a2;
    // check that the value is correct
    static_assert(q2 == 5.0);

    // check that the values of the two quadratic forms can be subtracted
    static_assert(q1 - q2 == 0.0);

    // all done
    return 0;
}


// end of file
