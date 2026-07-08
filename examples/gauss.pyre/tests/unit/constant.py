#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


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
    points = [0, 0.25, 0.5, 0.75, 1.0]
    # exercise the behavior
    assert list(const.eval(points)) == [value] * len(points)
    # and return it
    return const


# main
if __name__ == "__main__":
    test()


# end of file
