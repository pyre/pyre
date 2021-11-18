// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 2021 all rights reserved
//

// system includes
#include <iostream>
#include <cassert>

// dependencies
#include <pyre/algebra.h>

using namespace pyre::algebra;

// main program
int main(int argc, char* argv[]) {

    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("tensor_print");

    // make a channel
    pyre::journal::info_t channel("pyre.grid.tensor");

    matrix_t<1, 1> A { 1 };
    channel << A << pyre::journal::endl;

    matrix_t<1, 2> B { 0, 1 };
    channel << B << pyre::journal::endl;

    matrix_t<2, 1> C { 0, 1 };
    channel << C << pyre::journal::endl;

    matrix_t<2, 2> D { 0, 1, 2, 3 };
    channel << D << pyre::journal::endl;

    matrix_t<3, 3> E { 0, 1, 2, 3, 4, 5, 6, 7, 8 };
    channel << E << pyre::journal::endl;

    vector_t<1> a { 1 };
    channel << a << pyre::journal::endl;

    vector_t<2> b { 1, 1 };
    channel << b << pyre::journal::endl;

    vector_t<3> c { 1, 1, 1 };
    channel << c << pyre::journal::endl;

    // all done
    return 0;
}

// end of file
