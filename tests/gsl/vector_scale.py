#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Sanity check: verify that the vector object is accessible
"""


def test():
    # package access
    import gsl
    # make a couple of vectors and initialize them
    v = gsl.vector(shape=100).fill(value=1)
    # check
    for e in v: assert e == 1
    # add them and store the result in v1
    v *= 2
    # check
    for e in v: assert e == 2
    # all done
    return v


# main
if __name__ == "__main__":
    test()


# end of file 
