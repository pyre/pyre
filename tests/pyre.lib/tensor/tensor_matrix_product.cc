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
    // the packing-agnostic canonical basis of R^3x3
    constexpr auto e00 = matrix_t<3>::unit<0, 0>;
    constexpr auto e01 = matrix_t<3>::unit<0, 1>;
    constexpr auto e02 = matrix_t<3>::unit<0, 2>;
    constexpr auto e10 = matrix_t<3>::unit<1, 0>;
    constexpr auto e11 = matrix_t<3>::unit<1, 1>;
    constexpr auto e12 = matrix_t<3>::unit<1, 2>;
    constexpr auto e20 = matrix_t<3>::unit<2, 0>;
    constexpr auto e21 = matrix_t<3>::unit<2, 1>;
    constexpr auto e22 = matrix_t<3>::unit<2, 2>;

    // pick a matrix
    constexpr auto B = 1.0 * e00 + 0.0 * e01 + 0.0 * e02 + 0.0 * e10 + 2.0 * e11 + 0.0 * e12
                     + 0.0 * e20 + 0.0 * e21 + 3.0 * e22;

    // pick the matrix square
    constexpr auto B2 = 1.0 * e00 + 0.0 * e01 + 0.0 * e02 + 0.0 * e10 + 4.0 * e11 + 0.0 * e12
                      + 0.0 * e20 + 0.0 * e21 + 9.0 * e22;

    // verify matrix-matrix product
    static_assert(B * B == B2);

    // all done
    return 0;
}


// end of file
