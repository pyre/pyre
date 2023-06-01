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
    // 2D vector: canonical basis
    static_assert(vector_t<2>::unit<0> == vector_t<2> { 1, 0 });
    static_assert(vector_t<2>::unit<1> == vector_t<2> { 0, 1 });
    static_assert(vector_t<2>::unit<0> + vector_t<2>::unit<1> == vector_t<2>::ones);

    // 3D vector: canonical basis
    static_assert(vector_t<3>::unit<0> == vector_t<3> { 1, 0, 0 });
    static_assert(vector_t<3>::unit<1> == vector_t<3> { 0, 1, 0 });
    static_assert(vector_t<3>::unit<2> == vector_t<3> { 0, 0, 1 });
    static_assert(
        vector_t<3>::unit<0> + vector_t<3>::unit<1> + vector_t<3>::unit<2> == vector_t<3>::ones);

    // 2D matrix: canonical basis
    static_assert(matrix_t<2>::unit<0, 0> == matrix_t<2> { 1, 0, 0, 0 });
    static_assert(matrix_t<2>::unit<0, 1> == matrix_t<2> { 0, 1, 0, 0 });
    static_assert(matrix_t<2>::unit<1, 0> == matrix_t<2> { 0, 0, 1, 0 });
    static_assert(matrix_t<2>::unit<1, 1> == matrix_t<2> { 0, 0, 0, 1 });
    static_assert(
        matrix_t<2>::unit<0, 0> + matrix_t<2>::unit<0, 1> + matrix_t<2>::unit<1, 0>
            + matrix_t<2>::unit<1, 1>
        == matrix_t<2, 2>::ones);

    // 3D matrix: canonical basis
    static_assert(matrix_t<3>::unit<0, 0> == matrix_t<3> { 1, 0, 0, 0, 0, 0, 0, 0, 0 });
    static_assert(matrix_t<3>::unit<0, 1> == matrix_t<3> { 0, 1, 0, 0, 0, 0, 0, 0, 0 });
    static_assert(matrix_t<3>::unit<0, 2> == matrix_t<3> { 0, 0, 1, 0, 0, 0, 0, 0, 0 });
    static_assert(matrix_t<3>::unit<1, 0> == matrix_t<3> { 0, 0, 0, 1, 0, 0, 0, 0, 0 });
    static_assert(matrix_t<3>::unit<1, 1> == matrix_t<3> { 0, 0, 0, 0, 1, 0, 0, 0, 0 });
    static_assert(matrix_t<3>::unit<1, 2> == matrix_t<3> { 0, 0, 0, 0, 0, 1, 0, 0, 0 });
    static_assert(matrix_t<3>::unit<2, 0> == matrix_t<3> { 0, 0, 0, 0, 0, 0, 1, 0, 0 });
    static_assert(matrix_t<3>::unit<2, 1> == matrix_t<3> { 0, 0, 0, 0, 0, 0, 0, 1, 0 });
    static_assert(matrix_t<3>::unit<2, 2> == matrix_t<3> { 0, 0, 0, 0, 0, 0, 0, 0, 1 });
    static_assert(
        matrix_t<3>::unit<0, 0> + matrix_t<3>::unit<0, 1> + matrix_t<3>::unit<0, 2>
            + matrix_t<3>::unit<1, 0> + matrix_t<3>::unit<1, 1> + matrix_t<3>::unit<1, 2>
            + matrix_t<3>::unit<2, 0> + matrix_t<3>::unit<2, 1> + matrix_t<3>::unit<2, 2>
        == matrix_t<3, 3>::ones);

    // 2D vector: basis vectors are orthogonal
    static_assert(vector_t<2>::unit<0> * vector_t<2>::unit<1> == 0);

    // 3D vector: basis vectors are orthogonal
    static_assert(vector_t<3>::unit<0> * vector_t<3>::unit<1> == 0);
    static_assert(vector_t<3>::unit<0> * vector_t<3>::unit<2> == 0);
    static_assert(vector_t<3>::unit<1> * vector_t<3>::unit<2> == 0);

    // the packing-agnostic canonical basis of R^2x2
    constexpr auto e_00 = matrix_t<2>::unit<0, 0>;
    constexpr auto e_01 = matrix_t<2>::unit<0, 1>;
    constexpr auto e_10 = matrix_t<2>::unit<1, 0>;
    constexpr auto e_11 = matrix_t<2>::unit<1, 1>;
    // the out-of-diagonal basis element for symmetric matrices
    constexpr auto e_01_sym = symmetric_matrix_t<2>::unit<1, 2>;

    // assert diagonal basis matrices are diagonal (therefore symmetric)
    static_assert(e_00.is_diagonal() && e_00.is_symmetric());
    static_assert(e_11.is_diagonal() && e_11.is_symmetric());

    // summing diagonal matrices results in a symmetric and diagonal matrix
    static_assert((e_00 + e_11).is_diagonal() && (e_00 + e_11).is_symmetric());

    // assert out-of-diagonal basis matrices are neither symmetric nor diagonal
    static_assert(!e_01.is_diagonal() && !e_01.is_symmetric());
    static_assert(!e_10.is_diagonal() && !e_10.is_symmetric());

    // diagonal + nonsymmetric = nondiagonal and nonsymmetric
    static_assert(!(e_00 + e_01).is_diagonal() && !(e_00 + e_01).is_symmetric());
    static_assert(!(e_00 + e_10).is_diagonal() && !(e_00 + e_10).is_symmetric());
    static_assert(!(e_11 + e_01).is_diagonal() && !(e_11 + e_01).is_symmetric());
    static_assert(!(e_11 + e_10).is_diagonal() && !(e_11 + e_10).is_symmetric());

    // assert that the out-of-diagonal basis element for symmetric matrices is not diagonal
    //  but is symmetric
    static_assert(!e_01_sym.is_diagonal() && e_01_sym.is_symmetric());

    // assert diagonal + symmetric = nondiagonal and symmetric
    static_assert(!(e_00 + e_01_sym).is_diagonal() && (e_00 + e_01_sym).is_symmetric());
    static_assert(!(e_11 + e_01_sym).is_diagonal() && (e_11 + e_01_sym).is_symmetric());

    // other types that cast to double
    static_assert(
        true * e_00 + 2.0 * e_01 + 3.0 * e_10 + 4 * e_11
        == e_00 + 2.0 * e_01 + 3.0 * e_10 + 4.0 * e_11);

    // all done
    return 0;
}


// end of file
