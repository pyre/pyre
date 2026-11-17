#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the truncated gaussian: sampling stays inside the support, the density matches the
analytic normalized gaussian, and degenerate parameters are rejected
"""


def test():
    # support
    from math import erfc, exp, pi, sqrt

    # get the package
    import gsl

    # the standard normal cdf
    def Phi(z):
        """
        The standard normal cumulative distribution at {z}
        """
        # via the complementary error function
        return 0.5 * erfc(-z / sqrt(2))

    # a plain gaussian density
    def gaussian(x, mean, sigma):
        """
        The density at {x} of the gaussian with the given {mean} and {sigma}
        """
        # normalized over the whole line
        return exp(-0.5 * ((x - mean) / sigma) ** 2) / (sigma * sqrt(2 * pi))

    # the parameters: the center and width of the gaussian
    mean, sigma = 1.0, 2.0
    # the ends of the support, asymmetric about the mean, so a swapped or sign-flipped endpoint
    # would show
    a, b = -1.0, 4.0
    # which form the support
    support = (a, b)

    # the mass the truncation retains
    mass = Phi((b - mean) / sigma) - Phi((a - mean) / sigma)

    # make a generator
    rng = gsl.rng()
    # and the distribution
    tg = gsl.pdf.tgaussian(mean=mean, sigma=sigma, support=support, rng=rng)

    # the density matches the analytic value, at the mean and at an off-center point
    for x in (mean, 2.5):
        # where the truncated density is the plain one scaled by the retained mass
        expected = gaussian(x, mean, sigma) / mass
        # and the two agree
        assert abs(tg.density(x) - expected) < 1e-12

    # there is no mass below the support
    assert tg.density(a - 1.0) == 0.0
    # or above it
    assert tg.density(b + 1.0) == 0.0

    # a single sample lands inside the support
    assert a <= tg.sample() <= b

    # make a vector
    v = gsl.vector(shape=1000)
    # fill it with samples
    tg.vector(vector=v)
    # all of which land inside the support
    assert all(a <= v[i] <= b for i in range(v.shape))

    # make a matrix
    m = gsl.matrix(shape=(50, 20))
    # fill it with samples
    tg.matrix(matrix=m)
    # get its shape
    rows, columns = m.shape
    # and check that every sample lands inside the support
    assert all(a <= m[i, j] <= b for i in range(rows) for j in range(columns))

    # a nonpositive width is rejected
    try:
        # sample from a distribution of zero width
        gsl.pdf.tgaussian(mean=mean, sigma=0.0, support=support, rng=rng).sample()
    # which is what should happen
    except ValueError:
        # so there is nothing else to check
        pass
    # and if it doesn't
    else:
        # the guard is gone
        assert False, "a zero width was not rejected"

    # an empty support is rejected
    try:
        # sample from a distribution whose support has its ends reversed
        gsl.pdf.tgaussian(mean=mean, sigma=sigma, support=(b, a), rng=rng).sample()
    # which is what should happen
    except ValueError:
        # so there is nothing else to check
        pass
    # and if it doesn't
    else:
        # the guard is gone
        assert False, "an empty support was not rejected"

    # all done
    return tg


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
