#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Swap two rows of a matrix, naming the second with a reflected negative index
"""


def test():
    # get the package
    import gsl

    # an asymmetric matrix, so a swap of rows cannot be confused with a swap of columns
    m = gsl.matrix(shape=(3, 4))
    for row in range(3):
        for column in range(4):
            m[row, column] = row * 4 + column

    # swap the first row with the last, naming the last with a negative index
    m.swapRows(0, -1)

    # the last row's cells now sit in the first, and the first row's in the last
    assert m[0, 1] == 9.0 and m[2, 1] == 1.0
    # the middle row is untouched
    assert m[1, 1] == 5.0

    # all done
    return m


# main
if __name__ == "__main__":
    test()


# end of file
