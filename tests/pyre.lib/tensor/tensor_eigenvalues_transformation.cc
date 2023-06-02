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
    static_assert(function(matrix_t<2>::zero, constexpr_exp) == matrix_t<2>::identity);

    // log(one) = zero
    static_assert(function(matrix_t<2>::identity, constexpr_log) == matrix_t<2>::zero);

    // exp(zero) = one
    static_assert(function(matrix_t<3>::zero, constexpr_exp) == matrix_t<3>::identity);

    // log(one) = zero
    static_assert(function(matrix_t<3>::identity, constexpr_log) == matrix_t<3>::zero);

    // all done
    return 0;
}


// end of file
