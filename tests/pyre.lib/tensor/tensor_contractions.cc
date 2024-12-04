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
    pyre::journal::application("tensor_contractions");

    // make a channel
    pyre::journal::info_t channel("pyre.tensor.tensor_contractions");

    // the contraction type resulting from a 2x5 matrix and a 5D vector
    using contraction_matrix_vector = contraction<matrix_t<2, 5>, vector_t<5>>::type;
    // check that the contraction is a 2D vector
    static_assert(std::is_same_v<contraction_matrix_vector, vector_t<2>>);

    // the contraction type resulting from a 2D vector and a 2x5 matrix
    using contraction_vector_matrix = contraction<vector_t<2>, matrix_t<2, 5>>::type;
    // check that the contraction is a 5D vector
    static_assert(std::is_same_v<contraction_vector_matrix, vector_t<5>>);

    // the contraction type resulting from fourth order tensor that maps 2x5 matrices into
    // 2x5 matrices and a 2x5 matrix
    using contraction_fourth_order_matrix =
        contraction<fourth_order_tensor_t<2, 5, 2, 5>, matrix_t<2, 5>>::type;
    // check that the contraction is a 2x5 matrix
    static_assert(std::is_same_v<contraction_fourth_order_matrix, matrix_t<2, 5>>);

    // all done
    return 0;
}


// end of file
