#!/usr/bin/env python3
# -*- Python -*-
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

    # the standard normal cdf, via the complementary error function
    def Phi(z):
        return 0.5 * erfc(-z / sqrt(2))

    # a plain gaussian density
    def gaussian(x, mean, sigma):
        return exp(-0.5 * ((x - mean) / sigma) ** 2) / (sigma * sqrt(2 * pi))

    # the parameters; the support is asymmetric about the mean, so a swapped or sign-flipped
    # endpoint would show
    mean, sigma = 1.0, 2.0
    a, b = -1.0, 4.0
    support = (a, b)

    # the mass the truncation retains
    mass = Phi((b - mean) / sigma) - Phi((a - mean) / sigma)

    # a generator and the distribution
    rng = gsl.rng()
    tg = gsl.pdf.tgaussian(mean=mean, sigma=sigma, support=support, rng=rng)

    # the density matches the analytic value, at the mean and at an off-center point
    for x in (mean, 2.5):
        expected = gaussian(x, mean, sigma) / mass
        assert abs(tg.density(x) - expected) < 1e-12

    # there is no mass outside the support
    assert tg.density(a - 1.0) == 0.0
    assert tg.density(b + 1.0) == 0.0

    # a single sample lands inside the support
    assert a <= tg.sample() <= b

    # a filled vector lands inside the support
    v = gsl.vector(shape=1000)
    tg.vector(vector=v)
    assert all(a <= v[i] <= b for i in range(v.shape))

    # so does a filled matrix
    m = gsl.matrix(shape=(50, 20))
    tg.matrix(matrix=m)
    rows, columns = m.shape
    assert all(a <= m[i, j] <= b for i in range(rows) for j in range(columns))

    # a nonpositive width is rejected
    try:
        gsl.pdf.tgaussian(mean=mean, sigma=0.0, support=support, rng=rng).sample()
    except ValueError:
        pass
    else:
        assert False, "a zero width was not rejected"

    # an empty support is rejected
    try:
        gsl.pdf.tgaussian(mean=mean, sigma=sigma, support=(b, a), rng=rng).sample()
    except ValueError:
        pass
    else:
        assert False, "an empty support was not rejected"

    # all done
    return tg


# main
if __name__ == "__main__":
    test()


# end of file
