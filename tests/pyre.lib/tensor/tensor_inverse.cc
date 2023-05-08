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

    // the packing-agnostic canonical basis of R^3
    constexpr auto e0 = vector_t<3>::unit<0>;
    constexpr auto e1 = vector_t<3>::unit<1>;
    constexpr auto e2 = vector_t<3>::unit<2>;

    // construct a matrix in R^3x3
    constexpr auto A = 1.0 * e00 - 2.0 * e01 + 0.0 * e02 + 0.0 * e10 + 1.0 * e11 + 2.0 * e12
                     + 0.0 * e20 + 1.0 * e21 + 1.0 * e22;
    // construct a vector in R^3x3
    constexpr auto x = 1.0 * e0 + 1.0 * e1 + 1.0 * e2;
    // pick a scalar
    constexpr auto a = -2.0;
    // construct a right-hand side {y} such that: aAx = y
    constexpr auto y = a * A * x;
    // solve the linear system for x
    static_assert(inverse(A) * y / a == x);

    // all done
    return 0;
}


// end of file
