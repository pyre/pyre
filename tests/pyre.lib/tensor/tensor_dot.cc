// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2024 all rights reserved
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
    pyre::journal::application("tensor_dot");

    // make a channel
    pyre::journal::info_t channel("pyre.tensor");

    // a canonical tensor
    constexpr auto tensor_1 = matrix_t<2, 2> { 1.0, 2.0, 3.0, 4.0 };

    // a symmetric tensor
    constexpr auto tensor_2 = symmetric_matrix_t<2> { -1.0, -2.0, -4.0 };

    // compute the dot product of {tensor_1} and {tensor_2}
    constexpr auto result = dot(tensor_1, tensor_2);

    // report
    channel << "tensor_1 = " << tensor_1 << pyre::journal::newline;
    channel << "tensor_2 = " << tensor_2 << pyre::journal::newline;
    channel << "dot(tensor_1, tensor_2) = " << result << pyre::journal::endl;

    // check the result
    static_assert(result == -27.0);

    // all done
    return 0;
}


// end of file
