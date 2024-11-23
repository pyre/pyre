// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2024 all rights reserved
//

// Constexpr implementation of transcendental functions until C++26 implements them

// code guard
#if !defined(pyre_math_transcendental_h)
#define pyre_math_transcendental_h


// TOFIX: switch to auto ->

namespace pyre::math {

    // function to compute factorial of an integer
    constexpr double factorial(int n);

    // {constexpr} pow for integer exponents
    constexpr double pow(double base, int exp);

    // {constexpr} exp function
    constexpr double exp(double x);

    // {constexpr} log function
    constexpr double log(double x);

    // {constexpr} sqrt function
    constexpr double sqrt(double x);

    // {constexpr} sin function
    constexpr double sin(double x);

    // {constexpr} cos function
    constexpr double cos(double x);

    // {constexpr} atan function
    constexpr double atan(double x);

    // {constexpr} atan2 function
    constexpr double atan2(double y, double x);

} // namespace pyre::math


// get the inline definitions
#define pyre_tensor_transcendental_icc
#include "transcendental.icc"
#undef pyre_tensor_transcendental_icc


#endif

// end of file
