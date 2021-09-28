// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2021 all rights reserved
//

// system includes
#include <iostream>
#include <cassert>

// dependencies
#include <pyre/algebra/Tensor.h>
#include <pyre/algebra/tensor_algebra.h>

// main program
int main(int argc, char* argv[]) {

    pyre::algebra::vector_t<2> vector1 = { 0.0, 0.0 };
    assert(vector1 == vector1);

    pyre::algebra::vector_t<2> vector2 = { 1.0, 2.0 };
    vector1 += vector2;
    assert(vector1 + vector2 == 2.0 * vector2);
    assert(vector2 - vector1 == 2.0 * (vector2 - vector1));
    assert(vector2 - vector2 == pyre::algebra::vector_t<2>::zero);
    assert(pyre::algebra::vector_t<2>::zero
        == pyre::algebra::vector_t<2>::one - pyre::algebra::vector_t<2>::one);

    pyre::algebra::scalar_t a = 1.0;
    assert(vector2 * a == vector2);
    assert(vector2 * (-a) == -vector2);
    assert(vector2 / a == vector2);
    assert(vector2 / (-a) == -vector2);

    pyre::algebra::vector_t<3> vector3 = { 1, 0, 0 };
    pyre::algebra::vector_t<3> vector4 = { 0, 1, 0 };
    assert(vector3 * vector4 == 0.0);

    pyre::algebra::scalar_t b(1.0);
    assert(2 * b == b + 1);
    assert(2 * b - true == b);

    // TODO: Add tests for all algebraic operators

    // Matrix-vector product
    pyre::algebra::tensor_t<3, 3> A = { 0, 1, 2, 3, 4, 5, 6, 7, 8 };
    pyre::algebra::vector_t<3> x = { 1, 1, 1 };
    pyre::algebra::vector_t<3> y = a * A * x;
    assert((y == a * pyre::algebra::vector_t<3> { 3, 12, 21 }));

    // all done
    return 0;
}


// end of file
