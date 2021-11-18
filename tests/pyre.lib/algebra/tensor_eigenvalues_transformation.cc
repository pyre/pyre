// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 2021 all rights reserved
//


// support
#include <cassert>
// get the tensor algebra
#include <pyre/algebra.h>


// use namespace for readability
using namespace pyre::algebra;


// main program
int main(int argc, char* argv[]) {

    // define constexpr versions of exp and log
    constexpr auto constexpr_exp = [](double x) { return exp(x); };
    constexpr auto constexpr_log = [](double x) { return log(x); };

    // exp(zero) = one
    static_assert(function(zero_matrix<2>, constexpr_exp) == identity_matrix<2>);

    // log(one) = zero
    static_assert(function(identity_matrix<2>, constexpr_log) == zero_matrix<2>);

    // exp(zero) = one
    static_assert(function(zero_matrix<3>, constexpr_exp) == identity_matrix<3>);

    // log(one) = zero
    static_assert(function(identity_matrix<3>, constexpr_log) == zero_matrix<3>);

    // all done
    return 0;
}


// end of file
