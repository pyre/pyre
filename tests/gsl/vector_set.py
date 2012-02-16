#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Exercising setting and getting individual vector elements
"""


def test():
    # package access
    import gsl
    # make a vector
    v = gsl.vector(shape=100)
    # set an element to some value
    v[50] = 10
    # verify it happened
    assert v[50] == 10
    # all done
    return v


# main
if __name__ == "__main__":
    test()


# end of file 
