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

#ifdef DEVELOP_MODE
    pyre::algebra::vector_t<2> vector1 = { 1.0, 2.0 };
    pyre::algebra::vector_t<2> vector2 = { 1.0, 2.0 };
    pyre::algebra::vector_t<2> vector3 = { 1.0, 2.0 };
    pyre::algebra::vector_t<2> vector4 = { 1.0, 2.0 };
    pyre::algebra::vector_t<2> vector5 = { 1.0, 2.0 };

    auto vector_res = 2.0 * (vector1 - vector2 + vector3 - vector4 + vector5) / 2.0;
    assert(pyre::algebra::vector_t<2>::_constructor_calls 
        == 5 /* five constructors */ + 1 /* one temporary */);

    assert(vector_res == vector1);
#endif
    
    // all done
    return 0;
}

// end of file
