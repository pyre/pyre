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
    # make a vector
    v = gsl.vector(size=100)
    # set it to some value
    v.fill(value=2)
    # verify it happened
    for e in v: assert e == 2
    # all done
    return v


# main
if __name__ == "__main__":
    test()


# end of file 
