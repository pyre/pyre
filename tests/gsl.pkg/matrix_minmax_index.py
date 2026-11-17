#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Locate the smallest and the largest cell of a matrix, as a {row, column} pair
"""


def test():
    # get the package
    import gsl

    # an asymmetric matrix; the extrema sit at off-diagonal cells with distinct rows and columns,
    # so a transposed coordinate is caught
    m = gsl.matrix(shape=(3, 4))
    # go through its rows
    for row in range(3):
        # and its columns
        for column in range(4):
            # and number the cells in row major order
            m[row, column] = row * 4 + column
    # put the largest cell in the top right
    m[0, 3] = 99.0
    # and the smallest in the bottom left
    m[2, 0] = -7.0

    # the largest cell is at {row 0, column 3}
    assert m.maxIndex() == (0, 3)
    # the smallest cell is at {row 2, column 0}
    assert m.minIndex() == (2, 0)

    # all done
    return m


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
