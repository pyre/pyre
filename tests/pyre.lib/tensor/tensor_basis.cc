// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 2021 all rights reserved
//


// support
#include <cassert>
// get the tensor algebra
#include <pyre/tensor.h>


// use namespace for readability
using namespace pyre::tensor;


// main program
int main(int argc, char* argv[]) {

    // 2D vector: canonical basis
    static_assert(vector_t<2>::unit<0> == vector_t<2>{1, 0});
    static_assert(vector_t<2>::unit<1> == vector_t<2>{0, 1});
    static_assert(vector_t<2>::unit<0> + vector_t<2>::unit<1> == vector_t<2>::ones);

    // 3D vector: canonical basis
    static_assert(vector_t<3>::unit<0> == vector_t<3>{1, 0, 0});
    static_assert(vector_t<3>::unit<1> == vector_t<3>{0, 1, 0});
    static_assert(vector_t<3>::unit<2> == vector_t<3>{0, 0, 1});
    static_assert(vector_t<3>::unit<0> + vector_t<3>::unit<1> + vector_t<3>::unit<2> 
        == vector_t<3>::ones);

    // // 2D matrix: canonical basis
    static_assert(matrix_t<2>::unit<0, 0> == matrix_t<2>{1, 0, 0, 0});
    static_assert(matrix_t<2>::unit<0, 1> == matrix_t<2>{0, 1, 0, 0});
    static_assert(matrix_t<2>::unit<1, 0> == matrix_t<2>{0, 0, 1, 0});
    static_assert(matrix_t<2>::unit<1, 1> == matrix_t<2>{0, 0, 0, 1});
    static_assert(
          matrix_t<2>::unit<0, 0> + matrix_t<2>::unit<0, 1>
        + matrix_t<2>::unit<1, 0> + matrix_t<2>::unit<1, 1>
        == matrix_t<2, 2>::ones);

    // 3D matrix: canonical basis
    static_assert(matrix_t<3>::unit<0, 0> == matrix_t<3>{1, 0, 0, 0, 0, 0, 0, 0, 0});
    static_assert(matrix_t<3>::unit<0, 1> == matrix_t<3>{0, 1, 0, 0, 0, 0, 0, 0, 0});
    static_assert(matrix_t<3>::unit<0, 2> == matrix_t<3>{0, 0, 1, 0, 0, 0, 0, 0, 0});
    static_assert(matrix_t<3>::unit<1, 0> == matrix_t<3>{0, 0, 0, 1, 0, 0, 0, 0, 0});
    static_assert(matrix_t<3>::unit<1, 1> == matrix_t<3>{0, 0, 0, 0, 1, 0, 0, 0, 0});
    static_assert(matrix_t<3>::unit<1, 2> == matrix_t<3>{0, 0, 0, 0, 0, 1, 0, 0, 0});
    static_assert(matrix_t<3>::unit<2, 0> == matrix_t<3>{0, 0, 0, 0, 0, 0, 1, 0, 0});
    static_assert(matrix_t<3>::unit<2, 1> == matrix_t<3>{0, 0, 0, 0, 0, 0, 0, 1, 0});
    static_assert(matrix_t<3>::unit<2, 2> == matrix_t<3>{0, 0, 0, 0, 0, 0, 0, 0, 1});
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

    // all done
    return 0;
}


// end of file
