#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Exercise multiplying every vector element by a constant
"""


def test():
    # package access
    import gsl
    # make a vectors and initialize it
    v = gsl.vector(shape=100).fill(value=1)
    # check
    for e in v: assert e == 1
    # scale it
    v *= 2
    # check
    for e in v: assert e == 2
    # all done
    return v


# main
if __name__ == "__main__":
    test()


# end of file 
