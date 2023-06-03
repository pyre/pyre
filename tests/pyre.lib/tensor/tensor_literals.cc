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
    // vector: zero + one == one
    static_assert(zero<vector_t<2>> + ones<vector_t<2>> == ones<vector_t<2>>);
    static_assert(zero<vector_t<3>> + ones<vector_t<3>> == ones<vector_t<3>>);

    // vector: zero == one - one
    static_assert(zero<vector_t<2>> == ones<vector_t<2>> - ones<vector_t<2>>);
    static_assert(zero<vector_t<3>> == ones<vector_t<3>> - ones<vector_t<3>>);

    // matrix: zero + one == one
    static_assert(zero<matrix_t<2>> + ones<matrix_t<2>> == ones<matrix_t<2>>);
    static_assert(zero<matrix_t<3>> + ones<matrix_t<3>> == ones<matrix_t<3>>);

    // matrix: zero == one - one
    static_assert(zero<matrix_t<2>> == ones<matrix_t<2>> - ones<matrix_t<2>>);
    static_assert(zero<matrix_t<3>> == ones<matrix_t<3>> - ones<matrix_t<3>>);

    // all done
    return 0;
}


// end of file
