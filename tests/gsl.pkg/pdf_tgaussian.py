#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Lijun Zhu
# Caltech
# (c) 1998-2026 all rights reserved
#


"""
Exercise the truncated gaussian pdf
"""


def test():
    # math
    from math import pi, sqrt, exp, erfc
    # access the package
    import gsl

    # parameters
    mean = 1.0
    sigma = 2.0
    support = (-1.0, 3.0)
    a, b = support

    # Gaussian CDF via erfc: Phi(x) = 0.5 * erfc(-x / sqrt(2))
    def normal_cdf(x):
        return 0.5 * erfc(-x / sqrt(2))

    def gaussian_pdf(x, mu, sig):
        return exp(-0.5 * ((x - mu) / sig)**2) / (sig * sqrt(2 * pi))

    # build a random number generator
    rng = gsl.rng()
    # build a truncated gaussian distribution
    tg = gsl.pdf.tgaussian(mean=mean, sigma=sigma, support=support, rng=rng)

    # sample it and check it falls within [a, b]
    sample = tg.sample()
    assert a <= sample <= b

    # compute the density at x = mean
    # PDF(x) = gaussian_pdf(x, mean, sigma) / (CDF(b) - CDF(a))
    pa = normal_cdf((a - mean) / sigma)
    pb = normal_cdf((b - mean) / sigma)
    x = mean
    expected = gaussian_pdf(x, mean, sigma) / (pb - pa)
    assert abs(tg.density(x) - expected) < 1e-12

    # density outside support must be zero
    assert tg.density(a - 1.0) == 0.0
    assert tg.density(b + 1.0) == 0.0

    # make a vector and fill it
    v = gsl.vector(1000)
    tg.vector(vector=v)
    # all samples must be within [a, b]
    for sample in v:
        assert a <= sample <= b

    # make a matrix and fill it
    m = gsl.matrix(shape=(50, 200))
    tg.matrix(matrix=m)
    # all samples must be within [a, b]
    for sample in m:
        assert a <= sample <= b

    return tg


# main
if __name__ == "__main__":
    test()


# end of file
