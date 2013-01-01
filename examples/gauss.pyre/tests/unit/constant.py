#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


"""
Sanity check: verify that the constant functor behaves as expected
"""


def test():
    import gauss

    # pick a value
    value = 2
    # instantiate
    const = gauss.functors.constant(name="const")
    const.value = value
    # set up some points
    points = [0, .25, .5, .75, 1.]
    # exercise the behavior
    assert list(const.eval(points)) == [value]*len(points)
    # and return it
    return const


# main
if __name__ == "__main__":
    test()


# end of file 
