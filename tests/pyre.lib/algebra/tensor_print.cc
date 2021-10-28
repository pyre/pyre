// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 2021 all rights reserved
//

// system includes
#include <iostream>
#include <cassert>

// dependencies
#include <pyre/algebra/Tensor.h>
#include <pyre/algebra/tensor_algebra.h>

using namespace pyre::algebra;

// main program
int main(int argc, char* argv[]) {

    matrix_t<1, 1> A = { 1 };
    std::cout << A << std::endl;

    matrix_t<1, 2> B = { 0, 1 };
    std::cout << B << std::endl;

    matrix_t<2, 1> C = { 0, 1 };
    std::cout << C << std::endl;

    matrix_t<2, 2> D = { 0, 1, 2, 3 };
    std::cout << D << std::endl;

    matrix_t<3, 3> E = { 0, 1, 2, 3, 4, 5, 6, 7, 8 };
    std::cout << E << std::endl;

    vector_t<1> a = { 1 };
    std::cout << a << std::endl;

    vector_t<2> b = { 1, 1 };
    std::cout << b << std::endl;

    vector_t<3> c = { 1, 1, 1 };
    std::cout << c << std::endl;

    // all done
    return 0;
}

// end of file
