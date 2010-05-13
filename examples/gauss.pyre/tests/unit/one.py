#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Sanity check: verify that the unit functor behaves as expected
"""


def test():
    import gauss.functors

    # instantiate
    one = gauss.functors.one(name="one")
    # set up some points
    points = [0, .25, .5, .75, 1.]
    # exercise the behavior
    assert list(one.eval(points)) == [1]*len(points)
    # and return it
    return one


# main
if __name__ == "__main__":
    test()


# end of file 
