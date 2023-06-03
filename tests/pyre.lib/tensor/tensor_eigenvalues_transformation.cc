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
    // define constexpr versions of exp and log
    constexpr auto constexpr_exp = [](double x) {
        return exp(x);
    };
    constexpr auto constexpr_log = [](double x) {
        return log(x);
    };

    // exp(zero) = one
    static_assert(function(zero<matrix_t<2>>, constexpr_exp) == identity<matrix_t<2>>);

    // log(one) = zero
    static_assert(function(identity<matrix_t<2>>, constexpr_log) == zero<matrix_t<2>>);

    // exp(zero) = one
    static_assert(function(zero<matrix_t<3>>, constexpr_exp) == identity<matrix_t<3>>);

    // log(one) = zero
    static_assert(function(identity<matrix_t<3>>, constexpr_log) == zero<matrix_t<3>>);

    // all done
    return 0;
}


// end of file
