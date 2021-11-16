// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 2021 all rights reserved
//

// support
#include <cassert>

// get the tensor algebra
#include <pyre/algebra/tensor_algebra.h>

// use namespace for readability
using namespace pyre::algebra;

// main program
int main(int argc, char* argv[]) {

    // 2D symmetric matrix
    constexpr symmetric_matrix_t<2> C = { 1, 2, /*2,*/ 2 };

    // QUESTION: How can these be constexpr if exp and log are not?
    constexpr auto constexpr_exp = [](double x) { return exp(x); };
    constexpr auto constexpr_log = [](double x) { return log(x); };
    constexpr auto C_exp = function(C, constexpr_exp);
    
    // TOFIX: remove, this just proves the point that C_exp is constexpr
    static_assert(C_exp[{0, 1}] == C_exp[{1, 0}]);

    // TOFIX:
    // static_assert(function(function(C, constexpr_exp), constexpr_log) == C);
    // static_assert(is_equal(function(function(C, my_exp), my_log), C));

    // TOFIX: this does not build
    // function(C, epsilon)
    // but this does 
    // function(C, epsilon<real>)

    // QUESTION: This can't be constexpr'ed
    auto C_exp2 = function(C, exp);

    // TOFIX: this does not build because of 0 / 0 in eigenvector calculation
    // exp(zero) = one
    // static_assert(function(zero_matrix<3>, constexpr_exp) == identity_matrix<3>);

    // all done
    return 0;
}

// end of file
