#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Exercise the gaussian pdf
"""


def test():
    # math
    from math import pi, sqrt, exp
    # access the package
    import gsl

    # the σ of the distribution
    σ = 2
    # build a random number generator
    rng = gsl.rng()
    # build a gaussian distribution
    gaussian = gsl.pdf.gaussian(σ)

    # sample it
    sample = gaussian.sample(rng)

    # compute the density
    x = 0
    density = gaussian.density(x)
    assert density == 1/sqrt(2*pi*σ**2) * exp(-x**2/ (2*σ**2))

    return gaussian


# main
if __name__ == "__main__":
    test()


# end of file 
