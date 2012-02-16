#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Set a matrix element to some value and verify it can be retrieved correctly
"""


def test():
    # package access
    import gsl
    # make a vector
    m = gsl.matrix(shape=(100, 100))
    # set an element to some value
    m[50,50] = 10
    # verify it happened
    assert m[50,50] == 10
    # all done
    return m


# main
if __name__ == "__main__":
    test()


# end of file 
