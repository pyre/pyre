#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


"""
Exercise in-place subtraction of matrices
"""


def test():
    # package access
    import gsl
    # make a couple of matrices and initialize them
    m1 = gsl.matrix(shape=(100,100)).fill(value=1)
    m2 = gsl.matrix(shape=(100,100)).fill(value=2)
    # check
    for e in m1: assert e == 1
    for e in m2: assert e == 2
    # subtract them and store the result in m2
    m2 -= m1
    # check
    for e in m1: assert e == 1
    for e in m2: assert e == 1
    # all done
    return m1, m2


# main
if __name__ == "__main__":
    test()


# end of file
