// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2025 all rights reserved
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
    // 2x2 diagonal matrix
    {
        // the packing-agnostic canonical basis of R^2x2
        constexpr auto e00 = unit<matrix_t<2>, 0, 0>;
        constexpr auto e11 = unit<matrix_t<2>, 1, 1>;

        // construct a diagonal matrix in R^2x2
        constexpr auto D = 1.0 * e00 + 2.0 * e11;
        // construct the inverse of matrix
        constexpr auto D_inv = 1.0 * e00 + (1.0 / 2.0) * e11;
        // check that the inverse calculation is correct
        static_assert(inverse(D) == D_inv);
    }

    // 3x3 diagonal matrix
    {
        // the packing-agnostic canonical basis of R^3x3
        constexpr auto e00 = unit<matrix_t<3>, 0, 0>;
        constexpr auto e11 = unit<matrix_t<3>, 1, 1>;
        constexpr auto e22 = unit<matrix_t<3>, 2, 2>;

        // construct a diagonal matrix in R^3x3
        constexpr auto D = 1.0 * e00 + 2.0 * e11 + 3.0 * e22;
        // construct the inverse of matrix
        constexpr auto D_inv = 1.0 * e00 + (1.0 / 2.0) * e11 + (1.0 / 3.0) * e22;
        // check that the inverse calculation is correct
        static_assert(inverse(D) == D_inv);
    }

    // all done
    return 0;
}


// end of file
