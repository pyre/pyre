// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2024 all rights reserved
//


// dependencies
#include <pyre/tensor.h>

using namespace pyre::tensor;

// main program
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("tensor_concepts");

    // make a channel
    pyre::journal::info_t channel("pyre.tensor.tensor_concepts");

    // a 1x1 matrix is a (n improper) matrix
    static_assert(matrix_c<matrix_t<1, 1>> == true);

    // a 1x1 matrix is a scalar
    static_assert(scalar_c<matrix_t<1, 1>> == true);

    // a 1x1 matrix is not a vector
    static_assert(vector_c<matrix_t<1, 1>> == false);

    // a 1x2 matrix is a (n improper) matrix
    static_assert(matrix_c<matrix_t<1, 2>> == true);

    // a 1x2 matrix is not a vector
    static_assert(vector_c<matrix_t<1, 2>> == false);

    // a 2x1 matrix is a (n improper) matrix
    static_assert(matrix_c<matrix_t<2, 1>> == true);

    // a 2x1 matrix is a not vector
    static_assert(vector_c<matrix_t<2, 1>> == false);

    // a 2x2 matrix is a (proper) matrix
    static_assert(matrix_c<matrix_t<2, 2>> == true);

    // a 2x2 matrix is a not vector
    static_assert(vector_c<matrix_t<2, 2>> == false);

    // a 1D vector is a not matrix
    static_assert(matrix_c<vector_t<1>> == false);

    // a 1D vector is a (n improper) vector
    static_assert(vector_c<vector_t<1>> == true);

    // a 2D vector is a not matrix
    static_assert(matrix_c<vector_t<2>> == false);

    // a 2D vector is a (proper) vector
    static_assert(vector_c<vector_t<2>> == true);

    // a 1x1 symmetric matrix is a (n improper) matrix
    static_assert(matrix_c<symmetric_matrix_t<1>> == true);

    // a 1x1 symmetric matrix is not a vector
    static_assert(vector_c<symmetric_matrix_t<1>> == false);

    // a 1x1 diagonal matrix is a (n improper) matrix
    static_assert(matrix_c<diagonal_matrix_t<1>> == true);

    // a 1x1 diagonal matrix is not a vector
    static_assert(vector_c<diagonal_matrix_t<1>> == false);

    // a 2x2 symmetric matrix is a (proper) matrix
    static_assert(matrix_c<symmetric_matrix_t<2>> == true);

    // a 2x2 symmetric matrix is not a vector
    static_assert(vector_c<symmetric_matrix_t<2>> == false);

    // a 2x2 diagonal matrix is a (proper) matrix
    static_assert(matrix_c<diagonal_matrix_t<2>> == true);

    // a 2x2 diagonal matrix is not a vector
    static_assert(vector_c<diagonal_matrix_t<2>> == false);

    // all done
    return 0;
}


// end of file
