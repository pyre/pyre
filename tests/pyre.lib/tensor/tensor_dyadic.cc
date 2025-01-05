// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2025 all rights reserved
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
    pyre::journal::application("tensor_dyadic");

    // make a channel
    pyre::journal::info_t channel("pyre.tensor");

    // a vector in 3D
    constexpr auto vector_1 = vector_t<3> { -2.0, 2.0, 10.0 };

    // a vector in 2D
    constexpr auto vector_2 = vector_t<2> { 1.0, -1.0 };

    // report
    channel << "v1 = " << vector_1 << pyre::journal::newline;
    channel << "v2 = " << vector_2 << pyre::journal::newline;
    channel << "dyadic(v1, v2) = " << dyadic(vector_1, vector_2) << pyre::journal::endl;

    // check the result
    static_assert(
        dyadic(vector_1, vector_2) == matrix_t<3, 2> { -2.0, 2.0, 2.0, -2.0, 10.0, -10.0 });

    // all done
    return 0;
}


// end of file
