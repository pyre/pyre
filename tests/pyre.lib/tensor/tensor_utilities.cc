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
    // 2D matrix: the columns of the identity are the canonical basis
    static_assert(col<0>(matrix_t<2>::identity) == vector_t<2>::unit<0>);
    static_assert(col<1>(matrix_t<2>::identity) == vector_t<2>::unit<1>);

    // 2D matrix: the rows of the identity are the canonical basis
    static_assert(row<0>(matrix_t<2>::identity) == vector_t<2>::unit<0>);
    static_assert(row<1>(matrix_t<2>::identity) == vector_t<2>::unit<1>);

    // 3D matrix: the columns of the identity are the canonical basis
    static_assert(col<0>(matrix_t<3>::identity) == vector_t<3>::unit<0>);
    static_assert(col<1>(matrix_t<3>::identity) == vector_t<3>::unit<1>);
    static_assert(col<2>(matrix_t<3>::identity) == vector_t<3>::unit<2>);

    // 3D matrix: the rows of the identity are the canonical basis
    static_assert(row<0>(matrix_t<3>::identity) == vector_t<3>::unit<0>);
    static_assert(row<1>(matrix_t<3>::identity) == vector_t<3>::unit<1>);
    static_assert(row<2>(matrix_t<3>::identity) == vector_t<3>::unit<2>);

    // 2D matrix: the diagonal of the identity is the ones vector
    static_assert(matrix_diagonal(matrix_t<2>::identity) == vector_t<2>::ones);

    // 3D matrix: the diagonal of the identity is the ones vector
    static_assert(matrix_diagonal(matrix_t<3>::identity) == vector_t<3>::ones);

    // 2D matrix: build a matrix with a given diagonal
    constexpr diagonal_matrix_t<2> matrix2D = matrix_diagonal(vector_t<2> { -1.0, 1.0 });

    // 2D matrix: the diagonal matrix built on the diagonal of a diagonal matrix is equal to the
    // diagonal matrix
    static_assert(matrix_diagonal(matrix_diagonal(matrix2D)) == matrix2D);

    // 3D matrix: build a matrix with a given diagonal
    constexpr diagonal_matrix_t<3> matrix3D = matrix_diagonal(vector_t<3> { -1.0, 1.0, 2.0 });

    // 3D matrix: the diagonal matrix built on the diagonal of a diagonal matrix is equal to the
    // diagonal matrix
    static_assert(matrix_diagonal(matrix_diagonal(matrix3D)) == matrix3D);

    // all done
    return 0;
}


// end of file
