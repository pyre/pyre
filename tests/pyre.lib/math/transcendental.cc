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
// {acos(0)} used to divide by zero and {acos(x < 0)} used to land outside [0, pi] with the wrong sign
static_assert(close(pyre::math::acos(0.0), pi / 2.0));
static_assert(close(pyre::math::acos(1.0), 0.0));
static_assert(close(pyre::math::acos(-1.0), pi));
static_assert(close(pyre::math::acos(0.5), pi / 3.0));
static_assert(close(pyre::math::acos(-0.5), 2.0 * pi / 3.0));

// verify the {acos(x) = pi/2 - asin(x)} identity holds at compile time across the domain
static_assert(close(pyre::math::acos(0.25) + pyre::math::asin(0.25), pi / 2.0));
static_assert(close(pyre::math::acos(-0.75) + pyre::math::asin(-0.75), pi / 2.0));


// main program
int
main(int argc, char * argv[])
{
    // exercise the same domain at run time, where the functions delegate to the standard library;
    // this pins the constexpr path to the runtime path so the two cannot silently diverge
    assert(close(pyre::math::asin(1.0), std::asin(1.0)));
    assert(close(pyre::math::asin(-1.0), std::asin(-1.0)));
    assert(close(pyre::math::asin(0.5), std::asin(0.5)));
    assert(close(pyre::math::acos(0.0), std::acos(0.0)));
    assert(close(pyre::math::acos(-0.5), std::acos(-0.5)));
    assert(close(pyre::math::acos(-1.0), std::acos(-1.0)));

    // out-of-domain inputs yield NaN, matching the standard library
    assert(std::isnan(pyre::math::asin(2.0)));
    assert(std::isnan(pyre::math::acos(-2.0)));

    // all done
    return 0;
}


// end of file
