// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// support
#include <cassert>
#include <cmath>
// get the constexpr transcendental functions
#include <pyre/math.h>


// compare two doubles to within an absolute tolerance
constexpr auto
close(double a, double b, double tol = 1.0e-9) -> bool
{
    // the signed difference
    const auto d = a - b;
    // its magnitude is within tolerance
    return (d < 0.0 ? -d : d) < tol;
}


// the constant pi, to full double precision
constexpr auto pi = M_PI;


// verify {asin} across its domain, endpoints included, at compile time
// the endpoints used to divide by zero in {atan(x / sqrt(1 - x^2))}, making them non-constexpr
static_assert(close(pyre::math::asin(0.0), 0.0));
static_assert(close(pyre::math::asin(1.0), pi / 2.0));
static_assert(close(pyre::math::asin(-1.0), -pi / 2.0));
static_assert(close(pyre::math::asin(0.5), pi / 6.0));
static_assert(close(pyre::math::asin(-0.5), -pi / 6.0));

// verify {acos} across its domain, endpoints included, at compile time
// {acos(0)} used to divide by zero and {acos(x < 0)} used to land outside [0, pi] with the wrong
// sign
static_assert(close(pyre::math::acos(0.0), pi / 2.0));
static_assert(close(pyre::math::acos(1.0), 0.0));
static_assert(close(pyre::math::acos(-1.0), pi));
static_assert(close(pyre::math::acos(0.5), pi / 3.0));
static_assert(close(pyre::math::acos(-0.5), 2.0 * pi / 3.0));

// verify the {acos(x) = pi/2 - asin(x)} identity holds at compile time across the domain
static_assert(close(pyre::math::acos(0.25) + pyre::math::asin(0.25), pi / 2.0));

// outside the domain, the compile time path yields NaN, just like the standard library does at
// run time; a NaN is the only value that differs from itself, which a constant expression can
// check without {std::isnan}
constexpr auto
nan(double x) -> bool
{
    // compare the value with itself
    return x != x;
}
static_assert(nan(pyre::math::asin(2.0)));
static_assert(nan(pyre::math::asin(-2.0)));
static_assert(nan(pyre::math::acos(2.0)));
static_assert(nan(pyre::math::acos(-2.0)));
static_assert(close(pyre::math::acos(-0.75) + pyre::math::asin(-0.75), pi / 2.0));


// main program
int
main(int argc, char * argv[])
{
    // the arguments, out of the compiler's reach: calls with literal arguments are evaluated
    // while compiling, which exercises the constexpr path again rather than the run time one
    volatile double zero = 0.0, one = 1.0, half = 0.5, two = 2.0;
    // exercise the same domain at run time, where the functions delegate to the standard library;
    // this pins the constexpr path to the runtime path so the two cannot silently diverge
    assert(close(pyre::math::asin(one), std::asin(1.0)));
    assert(close(pyre::math::asin(-one), std::asin(-1.0)));
    assert(close(pyre::math::asin(half), std::asin(0.5)));
    assert(close(pyre::math::acos(zero), std::acos(0.0)));
    assert(close(pyre::math::acos(-half), std::acos(-0.5)));
    assert(close(pyre::math::acos(-one), std::acos(-1.0)));

    // out-of-domain inputs yield NaN, matching the standard library
    assert(std::isnan(pyre::math::asin(two)));
    assert(std::isnan(pyre::math::acos(-two)));

    // all done
    return 0;
}


// end of file
