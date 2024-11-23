// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2024 all rights reserved
//

// Constexpr implementation of transcendental functions until C++26 implements them

// code guard
#if !defined(pyre_math_transcendental_h)
#define pyre_math_transcendental_h


namespace pyre::math {

    // function to compute factorial of an integer
    constexpr auto factorial(int n) -> double;

    // {constexpr} pow for integer exponents
    constexpr auto pow(double base, int exp) -> double;

    // {constexpr} exp function
    constexpr auto exp(double x) -> double;

    // {constexpr} log function
    constexpr auto log(double x) -> double;

    // {constexpr} sqrt function
    constexpr auto sqrt(double x) -> double;

    // {constexpr} sin function
    constexpr auto sin(double x) -> double;

    // {constexpr} cos function
    constexpr auto cos(double x) -> double;

    // {constexpr} atan function
    constexpr auto atan(double x) -> double;

    // {constexpr} atan2 function
    constexpr auto atan2(double y, double x) -> double;

} // namespace pyre::math


// get the inline definitions
#define pyre_tensor_transcendental_icc
#include "transcendental.icc"
#undef pyre_tensor_transcendental_icc


#endif

// end of file
