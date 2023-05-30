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

    // all done
    return 0;
}


// end of file
