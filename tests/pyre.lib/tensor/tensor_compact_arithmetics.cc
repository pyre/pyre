// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2023 all rights reserved
//

// support
#include <cassert>
#include <iostream>

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
    pyre::journal::application("tensor_packings_arithmetic");

    // make a channel
    pyre::journal::info_t channel("pyre.tensor");

    {
        // report
        channel << "canonical A, canonical B" << pyre::journal::newline;
        channel << pyre::journal::newline;

        // pick a matrix
        constexpr matrix_t<2, 2> A { 1.0, 2.0, 3.0, 4.0 };
        // pick a matrix
        constexpr matrix_t<2, 2> B { -1.0, 0.0, 0.0, -4.0 };

        // show me
        channel << "A = " << A << pyre::journal::newline;
        channel << "B = " << B << pyre::journal::newline;
        channel << pyre::journal::newline;

        // add temporary and reference
        channel << "(A + B) + B" << pyre::journal::newline;
        channel << (A + B) + B << pyre::journal::newline;
        channel << pyre::journal::newline;

        // add reference and temporary
        channel << "B + (A + B)" << pyre::journal::newline;
        channel << B + (A + B) << pyre::journal::newline;
        channel << pyre::journal::newline;

        // add temporary and temporary
        channel << "(A + B) + (A + B)" << pyre::journal::newline;
        channel << (A + B) + (A + B) << pyre::journal::newline;
        channel << pyre::journal::newline;
    }

    {
        // report
        channel << "diagonal A, canonical B" << pyre::journal::newline;
        channel << pyre::journal::newline;

        // pick a diagonal matrix
        constexpr diagonal_matrix_t<2> A { 1.0, 4.0 };
        // pick a matrix
        constexpr matrix_t<2, 2> B { -1.0, 0.0, 0.0, -4.0 };

        // show me
        channel << "A = " << A << pyre::journal::newline;
        channel << "B = " << B << pyre::journal::newline;
        channel << pyre::journal::newline;

        // add temporary and reference
        channel << "(A + B) + B" << pyre::journal::newline;
        channel << (A + B) + B << pyre::journal::newline;
        channel << pyre::journal::newline;

        // add reference and temporary
        channel << "B + (A + B)" << pyre::journal::newline;
        channel << B + (A + B) << pyre::journal::newline;
        channel << pyre::journal::newline;

        // add temporary and temporary
        channel << "(A + B) + (A + B)" << pyre::journal::newline;
        channel << (A + B) + (A + B) << pyre::journal::newline;
        channel << pyre::journal::newline;
    }

    {
        // report
        channel << "canonical A, diagonal B" << pyre::journal::newline;
        channel << pyre::journal::newline;

        // pick a matrix
        constexpr matrix_t<2, 2> A { 1.0, 0.0, 0.0, 4.0 };
        // pick a diagonal matrix
        constexpr diagonal_matrix_t<2> B { -1.0, -4.0 };

        // show me
        channel << "A = " << A << pyre::journal::newline;
        channel << "B = " << B << pyre::journal::newline;
        channel << pyre::journal::newline;

        // add temporary and reference
        channel << "(A + B) + B" << pyre::journal::newline;
        channel << (A + B) + B << pyre::journal::newline;
        channel << pyre::journal::newline;

        // add reference and temporary
        channel << "B + (A + B)" << pyre::journal::newline;
        channel << B + (A + B) << pyre::journal::newline;
        channel << pyre::journal::newline;

        // add temporary and temporary
        channel << "(A + B) + (A + B)" << pyre::journal::newline;
        channel << (A + B) + (A + B) << pyre::journal::newline;
        channel << pyre::journal::newline;
    }

    {
        // report
        channel << "diagonal A, diagonal B" << pyre::journal::newline;
        channel << pyre::journal::newline;

        // pick a diagonal matrix
        constexpr diagonal_matrix_t<2> A { 1.0, 4.0 };
        // pick a diagonal matrix
        constexpr diagonal_matrix_t<2> B { -1.0, -4.0 };

        // show me
        channel << "A = " << A << pyre::journal::newline;
        channel << "B = " << B << pyre::journal::newline;
        channel << pyre::journal::newline;

        // add temporary and reference
        channel << "(A + B) + B" << pyre::journal::newline;
        channel << (A + B) + B << pyre::journal::newline;
        channel << pyre::journal::newline;

        // add reference and temporary
        channel << "B + (A + B)" << pyre::journal::newline;
        channel << B + (A + B) << pyre::journal::newline;
        channel << pyre::journal::newline;

        // add temporary and temporary
        channel << "(A + B) + (A + B)" << pyre::journal::newline;
        channel << (A + B) + (A + B) << pyre::journal::newline;
        channel << pyre::journal::newline;
    }

    // flush
    channel << pyre::journal::endl(__HERE__);


    // all done
    return 0;
}


// end of file
