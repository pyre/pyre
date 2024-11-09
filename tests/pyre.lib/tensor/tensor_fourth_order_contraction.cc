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
    // construct a fourth-order tensor filled with ones
    constexpr auto C = ones<fourth_order_tensor_t<3, 3, 3, 3>>;

    // construct a matrix {A}
    constexpr auto a = 1.0;
    constexpr auto b = 2.0;
    constexpr auto c = -1.0;
    constexpr auto d = -3.0;
    constexpr auto e = 1.0;
    constexpr auto f = -1.0;
    constexpr auto A = matrix_t<3, 3> { a, d, e, d, b, f, e, f, c };

    // compute {B} as the contraction of {C} and {A}
    constexpr auto B = C * A;

    // check that each component of {B} equals the sum of all entries in {A}
    constexpr auto sum = a + b + c + 2.0 * d + 2.0 * e + 2.0 * f;
    static_assert((B[{ 0, 0 }] == sum));
    static_assert((B[{ 0, 1 }] == sum));
    static_assert((B[{ 0, 2 }] == sum));
    static_assert((B[{ 1, 0 }] == sum));
    static_assert((B[{ 1, 1 }] == sum));
    static_assert((B[{ 1, 2 }] == sum));
    static_assert((B[{ 2, 0 }] == sum));
    static_assert((B[{ 2, 1 }] == sum));
    static_assert((B[{ 2, 2 }] == sum));

    // all done
    return 0;
}


// end of file
