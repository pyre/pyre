#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2025 all rights reserved
#


"""
Exercise in-place matrix addition
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
    # add them and store the result in m1
    m1 += m2
    # check
    for e in m1: assert e == 3
    for e in m2: assert e == 2
    # all done
    return m1, m2


# main
if __name__ == "__main__":
    test()


# end of file
