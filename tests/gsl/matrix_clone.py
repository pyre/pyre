#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


"""
Copy a matrix
"""


def test():
    # package access
    import gsl
    # make a matrix
    m = gsl.matrix(shape=(100,50))
    # set it to random values
    m.random(pdf=gsl.pdf.gaussian(sigma=2, rng=gsl.rng()))
    # clone it
    n = m.clone()
    # and check it
    assert m == n

    # all done
    return m, n


# main
if __name__ == "__main__":
    test()


# end of file 
