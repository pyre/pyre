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

    // helper function to compute factorial
    constexpr double factorial(int n)
    {
        return (n <= 1) ? 1 : n * factorial(n - 1);
    }

    // helper function to compute power
    constexpr double pow_helper(double base, int exp)
    {
        return (exp == 0) ? 1 :
               (exp > 0)  ? base * pow_helper(base, exp - 1) :
                            1 / pow_helper(base, -exp);
    }

    // {constexpr} pow for integer exponents
    constexpr double pow(double base, int exp)
    {
        if (std::is_constant_evaluated()) {
            return pow_helper(base, exp);
        } else {
            return std::pow(base, exp);
        }
    }

    // helper function to compute the series sum
    constexpr double exp_series(double x, int terms = 15)
    {
        return (terms == 0) ? 1 : pow(x, terms) / factorial(terms) + exp_series(x, terms - 1);
    }

    // {constexpr} exp function
    constexpr double exp(double x)
    {
        if (std::is_constant_evaluated()) {
            return exp_series(x);
        } else {
            return std::exp(x);
        }
    }

    // helper function to compute log using Newton's method
    constexpr double log_newton(double x, double guess = 1.0, int iterations = 15)
    {
        return (iterations == 0) ?
                   guess :
                   log_newton(x, guess - (exp(guess) - x) / exp(guess), iterations - 1);
    }

    // {constexpr} log function
    constexpr double log_helper(double x)
    {
        return (x < 0)  ? std::numeric_limits<double>::quiet_NaN() :
               (x == 0) ? -std::numeric_limits<double>::infinity() :
               (x == 1) ? 0.0 :
                          log_newton(x);
    }

    // {constexpr} log function
    constexpr double log(double x)
    {
        if (std::is_constant_evaluated()) {
            return log_helper(x);
        } else {
            return std::log(x);
        }
    }

    // helper function to compute sqrt using Newton's method
    constexpr double sqrt_newton(double x, double guess = 1.0, int iterations = 15)
    {
        return (iterations == 0) ? guess :
                                   sqrt_newton(x, 0.5 * (guess + x / guess), iterations - 1);
    }

    // {constexpr} sqrt function
    constexpr double sqrt_helper(double x)
    {
        return (x < 0) ? std::numeric_limits<double>::quiet_NaN() : (x == 0) ? 0.0 : sqrt_newton(x);
    }

    // {constexpr} sqrt function
    constexpr double sqrt(double x)
    {
        if (std::is_constant_evaluated()) {
            return sqrt_helper(x);
        } else {
            return std::sqrt(x);
        }
    }

    // Taylor series expansion for sine
    constexpr double sin_taylor(double x, int terms = 15)
    {
        double result = 0.0;
        double power = x;
        for (int i = 0; i < terms; ++i) {
            int sign = (i % 2 == 0) ? 1 : -1;
            result += sign * power / factorial(2 * i + 1);
            power *= x * x;
        }
        return result;
    }

    // {constexpr} sin function
    constexpr double sin(double x)
    {
        if (std::is_constant_evaluated()) {
            return sin_taylor(x);
        } else {
            return std::sin(x);
        }
    }

    // Taylor series expansion for cosine
    constexpr double cos_taylor(double x, int terms = 15)
    {
        double result = 0.0;
        double power = 1.0;
        for (int i = 0; i < terms; ++i) {
            int sign = (i % 2 == 0) ? 1 : -1;
            result += sign * power / factorial(2 * i);
            power *= x * x;
        }
        return result;
    }

    // {constexpr} cos function
    constexpr double cos(double x)
    {
        if (std::is_constant_evaluated()) {
            return cos_taylor(x);
        } else {
            return std::cos(x);
        }
    }

    // Taylor series expansion for tangent
    constexpr double atan_poly(double x, int terms = 15)
    {
        if (x > 1.0) {
            return M_PI / 2 - atan(1 / x);
        } else if (x < -1.0) {
            return -M_PI / 2 - atan(1 / x);
        } else {
            double result = 0.0;
            double term = x;
            int sign = 1;
            for (int i = 1; i <= terms; ++i) {
                result += sign * term / (2 * i - 1);
                term *= x * x;
                sign = -sign;
            }
            return result;
        }
    }

    // {constexpr} atan function
    constexpr double atan(double x)
    {
        if (std::is_constant_evaluated()) {
            return atan_poly(x);
        } else {
            return std::atan(x);
        }
    }

    // Taylor series expansion for arctangent
    constexpr double atan2_poly(double y, double x)
    {
        if (x > 0) {
            return atan(y / x);
        } else if (x < 0 && y >= 0) {
            return atan(y / x) + M_PI;
        } else if (x < 0 && y < 0) {
            return atan(y / x) - M_PI;
        } else if (x == 0 && y > 0) {
            return M_PI / 2;
        } else if (x == 0 && y < 0) {
            return -M_PI / 2;
        }
        // undefined case when x == 0 and y == 0
        return 0.0;
    }

    // {constexpr} atan2 function
    constexpr double atan2(double y, double x)
    {
        if (std::is_constant_evaluated()) {
            return atan2_poly(y, x);
        } else {
            return std::atan2(y, x);
        }
    }

} // namespace pyre::math


#endif

// end of file
