#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Swap two of a vector's cells, naming the second with a reflected negative index
"""


def test():
    # get the package
    import gsl

    # an asymmetric vector, so the swap is visible
    v = gsl.vector(shape=4)
    v[0], v[1], v[2], v[3] = 3, 1, 4, 2

    # swap the first cell with the last, naming the last with a negative index
    v.swap(0, -1)

    # only those two cells move
    assert v.tuple() == (2.0, 1.0, 4.0, 3.0)

    # all done
    return v


# main
if __name__ == "__main__":
    test()


# end of file
