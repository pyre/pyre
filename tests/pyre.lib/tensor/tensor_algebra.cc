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
int main(int argc, char* argv[]) {

    // vector: zero + one == one
    static_assert(vector_t<2>::zero + vector_t<2>::ones == vector_t<2>::ones);
    static_assert(vector_t<3>::zero + vector_t<3>::ones == vector_t<3>::ones);

    // vector: zero == one - one
    static_assert(vector_t<2>::zero == vector_t<2>::ones - vector_t<2>::ones);
    static_assert(vector_t<3>::zero == vector_t<3>::ones - vector_t<3>::ones);

    // matrix: zero + one == one
    static_assert(matrix_t<2, 2>::zero + matrix_t<2, 2>::ones == matrix_t<2, 2>::ones);
    static_assert(matrix_t<3, 3>::zero + matrix_t<3, 3>::ones == matrix_t<3, 3>::ones);

    // matrix: zero == one - one
    static_assert(matrix_t<2, 2>::zero == matrix_t<2, 2>::ones - matrix_t<2, 2>::ones);
    static_assert(matrix_t<3, 3>::zero == matrix_t<3, 3>::ones - matrix_t<3, 3>::ones);

    // a scalar with negative one 
    constexpr scalar_t minus_one = -1.0;

    // vector: (-1) * v == - v
    static_assert(minus_one * vector_t<2>::ones == -vector_t<2>::ones);
    static_assert(vector_t<2>::ones * minus_one == -vector_t<2>::ones);
    static_assert(minus_one * vector_t<3>::ones == -vector_t<3>::ones);
    static_assert(vector_t<3>::ones * minus_one == -vector_t<3>::ones);

    // matrix: (-1) * A == - A
    static_assert(minus_one * matrix_t<2, 2>::ones == -matrix_t<2, 2>::ones);
    static_assert(matrix_t<2, 2>::ones * minus_one == -matrix_t<2, 2>::ones);
    static_assert(minus_one * matrix_t<3, 3>::ones == -matrix_t<3, 3>::ones);
    static_assert(matrix_t<3, 3>::ones * minus_one == -matrix_t<3, 3>::ones);

    // a 2D vector
    constexpr vector_t<2> vector2D { -2.0, 2.0 };

    // v + v == 2*v 
    static_assert(vector2D + vector2D == 2.0 * vector2D);

    // ( v + v ) / 2 == v 
    static_assert((vector2D + vector2D) / 2.0 == vector2D);

    // ( v + v ) / -2 == -v 
    static_assert((vector2D + vector2D) / -2.0 == -vector2D);

    // a 3D vector
    constexpr vector_t<3> vector3D { -2.0, 2.0, 10.0 };

    // v + v + v == 3 * v 
    static_assert(vector3D + vector3D + vector3D == 3.0 * vector3D);

    // ( v + v + v ) / 3 == v 
    static_assert((vector3D + vector3D + vector3D) / 3.0 == vector3D);

    // ( v + v + v ) / -3 == - v 
    static_assert((vector3D + vector3D + vector3D) / -3.0 == -vector3D);

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
