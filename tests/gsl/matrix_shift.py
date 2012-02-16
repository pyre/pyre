#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Exercise adding a constant to all elements of a matrix
"""


def test():
    # package access
    import gsl
    # make a couple of vectors and initialize them
    m = gsl.matrix(shape=(100,100)).fill(value=1)
    # check
    for e in m: assert e == 1
    # add them and store the result in v1
    m += 1
    # check
    for e in m: assert e == 2
    # all done
    return m


# main
if __name__ == "__main__":
    test()


# end of file 
