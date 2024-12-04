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
    // exp(zero) = one
    static_assert(function(zero<matrix_t<2>>, pyre::math::exp) == identity<matrix_t<2>>);

    // log(one) = zero
    static_assert(function(identity<matrix_t<2>>, pyre::math::log) == zero<matrix_t<2>>);

    // exp(zero) = one
    static_assert(function(zero<matrix_t<3>>, pyre::math::exp) == identity<matrix_t<3>>);

    // log(one) = zero
    static_assert(function(identity<matrix_t<3>>, pyre::math::log) == zero<matrix_t<3>>);

    // all done
    return 0;
}


// end of file
