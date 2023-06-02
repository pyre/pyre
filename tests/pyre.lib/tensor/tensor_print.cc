// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2023 all rights reserved
//


// system includes
#include <iostream>
// dependencies
#include <pyre/tensor.h>

using namespace pyre::tensor;

// main program
int
main(int argc, char * argv[])
{
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("tensor_print");

    // make a channel
    pyre::journal::info_t channel("pyre.tensor.tensor_print");

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

    symmetric_matrix_t<2> S { 0, 1, /*1, */ 2 };
    channel << "Tensor S: " << pyre::journal::newline;
    channel << pyre::journal::indent(1);
    channel << S << pyre::journal::newline;
    channel << "is symmetric = " << S.is_symmetric() << pyre::journal::newline;
    channel << "shape = " << S.shape() << pyre::journal::newline;
    channel << "data = " << pyre::journal::newline;
    channel << pyre::journal::indent(1);
    for (const auto s : S) {
        channel << s << pyre::journal::newline;
    }
    channel << pyre::journal::outdent(2) << pyre::journal::endl;

    diagonal_matrix_t<2> R { 0, 1 };
    channel << "Tensor R: " << pyre::journal::newline;
    channel << pyre::journal::indent(1);
    channel << R << pyre::journal::newline;
    channel << "is diagonal = " << R.is_diagonal() << pyre::journal::newline;
    channel << "is symmetric = " << R.is_symmetric() << pyre::journal::newline;
    channel << "shape = " << R.shape() << pyre::journal::newline;
    channel << "data = " << pyre::journal::newline;
    channel << pyre::journal::indent(1);
    for (const auto r : R) {
        channel << r << pyre::journal::newline;
    }
    channel << pyre::journal::outdent(2) << pyre::journal::endl;

    // all done
    return 0;
}


// end of file
