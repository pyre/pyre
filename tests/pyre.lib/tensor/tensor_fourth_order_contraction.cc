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
    }

    {
        // construct a fourth-order tensor
        constexpr auto C =
            fourth_order_tensor_t<2, 2, 2, 2> { 1.0, 2.0,  3.0,  4.0,  5.0,  6.0,  7.0,  8.0,
                                                9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0 };

        // construct a matrix {A}
        constexpr auto A = matrix_t<2, 2> { 1.0, 2.0, -1.0, -2.0 };

        // compute {B} as the contraction of {C} and {A}, {C} on the right
        constexpr auto B_right = A * C;

        // check that each component of {B} are correct
        static_assert((B_right[{ 0, 0 }] == -24.0));
        static_assert((B_right[{ 0, 1 }] == -24.0));
        static_assert((B_right[{ 1, 0 }] == -24.0));
        static_assert((B_right[{ 1, 1 }] == -24.0));

        // compute {B} as the contraction of {C} and {A}, {C} on the left
        constexpr auto B_left = C * A;

        // check that each component of {B} are correct
        static_assert((B_left[{ 0, 0 }] == -6.0));
        static_assert((B_left[{ 0, 1 }] == -6.0));
        static_assert((B_left[{ 1, 0 }] == -6.0));
        static_assert((B_left[{ 1, 1 }] == -6.0));
    }

    // all done
    return 0;
}


// end of file
