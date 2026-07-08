#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Sanity check: verify that the unit functor behaves as expected
"""


def test():
    import gauss

    # instantiate
    one = gauss.functors.one(name="one")
    # set up some points
    points = [0, 0.25, 0.5, 0.75, 1.0]
    # exercise the behavior
    assert list(one.eval(points)) == [1] * len(points)
    # and return it
    return one


# main
if __name__ == "__main__":
    test()


# end of file
