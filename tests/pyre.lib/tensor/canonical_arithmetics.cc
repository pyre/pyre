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
    // negative one
    constexpr scalar_t minus_one = -1.0;


    // vector R^2: (-1) * v == - v
    static_assert(minus_one * vector_t<2>::ones == -vector_t<2>::ones);
    // vector R^2: v * (-1) == - v
    static_assert(vector_t<2>::ones * minus_one == -vector_t<2>::ones);
    // vector R^3: v * (-1) == - v
    static_assert(minus_one * vector_t<3>::ones == -vector_t<3>::ones);
    // vector R^3: v * (-1) == - v
    static_assert(vector_t<3>::ones * minus_one == -vector_t<3>::ones);


    // matrix R^2x2: (-1) * A == - A
    static_assert(minus_one * matrix_t<2, 2>::ones == -matrix_t<2, 2>::ones);
    // matrix R^2x2: A * (-1) == - A
    static_assert(matrix_t<2, 2>::ones * minus_one == -matrix_t<2, 2>::ones);
    // matrix R^3x3: (-1) * A == - A
    static_assert(minus_one * matrix_t<3, 3>::ones == -matrix_t<3, 3>::ones);
    // matrix R^3x3: A * (-1) == - A
    static_assert(matrix_t<3, 3>::ones * minus_one == -matrix_t<3, 3>::ones);


    // a vector in R^2
    constexpr vector_t<2> vector2D { -2.0, 2.0 };
    // v + v == 2*v
    static_assert(vector2D + vector2D == 2.0 * vector2D);
    // ( v + v ) / 2 == v
    static_assert((vector2D + vector2D) / 2.0 == vector2D);
    // ( v + v ) / -2 == -v
    static_assert((vector2D + vector2D) / -2.0 == -vector2D);


    // a vector in R3
    constexpr vector_t<3> vector3D { -2.0, 2.0, 10.0 };
    // v + v + v == 3 * v
    static_assert(vector3D + vector3D + vector3D == 3.0 * vector3D);
    // ( v + v + v ) / 3 == v
    static_assert((vector3D + vector3D + vector3D) / 3.0 == vector3D);
    // ( v + v + v ) / -3 == - v
    static_assert((vector3D + vector3D + vector3D) / -3.0 == -vector3D);


    // a matrix in R^2x2
    constexpr matrix_t<2> matrix2D { -2.0, 2.0, -1.0, 0.0 };
    // A + A == 2*A
    static_assert(matrix2D + matrix2D == 2.0 * matrix2D);
    // ( A + A ) / 2 == A
    static_assert((matrix2D + matrix2D) / 2.0 == matrix2D);
    // ( A + A ) / -2 == -A
    static_assert((matrix2D + matrix2D) / -2.0 == -matrix2D);


    // a matrix in R^3x3
    constexpr matrix_t<3> matrix3D { -2.0, 2.0, -1.0, 0.0, -1.5, 0.1, -2.0, 1.0, 3.0 };
    // A + A + A == 3*A
    static_assert(matrix3D + matrix3D + matrix3D == 3.0 * matrix3D);
    // ( A + A + A ) / 3 == A
    static_assert((matrix3D + matrix3D + matrix3D) / 3.0 == matrix3D);
    // ( A + A + A) / -3 == -A
    static_assert((matrix3D + matrix3D + matrix3D) / -3.0 == -matrix3D);


    // all done
    return 0;
}


// end of file
