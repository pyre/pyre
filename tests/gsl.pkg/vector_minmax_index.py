#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Locate the smallest and the largest cell of a vector
"""


def test():
    # get the package
    import gsl

    # a vector with a unique min and a unique max at distinct cells
    v = gsl.vector(shape=5)
    v[0], v[1], v[2], v[3], v[4] = 3, 1, 4, 0, 5

    # the smallest cell is the zero at index 3
    assert v.minIndex() == 3
    # the largest cell is the five at index 4
    assert v.maxIndex() == 4

    # all done
    return v


# main
if __name__ == "__main__":
    test()


# end of file
