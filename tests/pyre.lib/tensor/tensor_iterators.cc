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
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("tensor_print");

    // make a channel
    pyre::journal::debug_t channel("pyre.tensor.tensor_iterators");

    // a 2D matrix
    matrix_t<2, 2> A { 1.0, 2.0, 3.0, 4.0 };
    channel << "Iterating on a 2x2 matrix:" << pyre::journal::newline;
    for (const auto a : A) {
        channel << "value = " << a << pyre::journal::newline;
    }
    channel << pyre::journal::newline;

    // a 2D symmetric matrix
    symmetric_matrix_t<2> B { 1.0, 2.0, 4.0 };
    channel << "Iterating on a symmetric 2x2 matrix:" << pyre::journal::newline;
    for (const auto b : B) {
        channel << "value = " << b << pyre::journal::newline;
    }
    channel << pyre::journal::newline;

    // a 2D diagonal matrix
    diagonal_matrix_t<2> C { 1.0, 2.0 };
    channel << "Iterating on a diagonal 2x2 matrix:" << pyre::journal::newline;
    for (const auto c : C) {
        channel << "value = " << c << pyre::journal::newline;
    }
    channel << pyre::journal::newline;

    // flush
    channel << pyre::journal::endl(__HERE__);


    // all done
    return 0;
}


// end of file
