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
    v = gsl.vector(size=100)
    # prime
    for index in range(v.size): v[index] = 2*index+1
    # find both the min and the max
    small, big = v.minmax()
    # check it
    assert small == 1
    assert big == 2*(v.size-1)+1
    # all done
    return v


# main
if __name__ == "__main__":
    test()


# end of file 
