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
    // vector a
    constexpr vector_t<3> a { -2.0, 2.0, 0.0 };

    // vector b
    constexpr vector_t<3> b { -1.0, 0.0, 2.0 };

    // vector c
    constexpr vector_t<3> c { -1.0, 1.0, 2.0 };

    // vector d
    constexpr vector_t<3> d { 0.0, 1.5, -1.5 };

    // scalar alpha
    constexpr scalar_t alpha = 5.0;

    // commutativity of addition
    static_assert(a + b == b + a);

    // commutativity of scalar product
    static_assert(a * b == b * a);

    // cross product of a vector with itself is zero
    static_assert(cross(a, a) == vector_t<3>::zero);

    // anti-commutativity of cross product
    static_assert(cross(a, b) == -cross(b, a));

    // distributivity of multiplication by a scalar over addition
    static_assert(alpha * (a + b) == alpha * a + alpha * b);

    // distributivity of scalar product over addition
    static_assert(c * (a + b) == c * a + c * b);

    // distributivity of vector product over addition:
    static_assert(cross(c, a + b) == cross(c, a) + cross(c, b));

    // scalar triple product
    static_assert(a * cross(b, c) == b * cross(c, a));

    // vector triple product
    static_assert(cross(a, cross(b, c)) == (a * c) * b - (a * b) * c);

    // Jacobi identity
    static_assert(
        cross(a, cross(b, c)) + cross(c, cross(a, b)) + cross(b, cross(c, a)) == vector_t<3>::zero);

    // Binet-Cauchy identity
    static_assert(cross(a, b) * cross(c, d) == (a * c) * (b * d) - (b * c) * (a * d));

    // all done
    return 0;
}


// end of file
