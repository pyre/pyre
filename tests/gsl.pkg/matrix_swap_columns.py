#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Swap two columns of a matrix, naming the second with a reflected negative index
"""


def test():
    # get the package
    import gsl

    # an asymmetric matrix, so a swap of columns cannot be confused with a swap of rows
    m = gsl.matrix(shape=(3, 4))
    for row in range(3):
        for column in range(4):
            m[row, column] = row * 4 + column

    # swap the first column with the last, naming the last with a negative index
    m.swapColumns(0, -1)

    # the last column's cells now sit in the first, and the first column's in the last
    assert m[1, 0] == 7.0 and m[1, 3] == 4.0
    # an untouched column stays put
    assert m[1, 1] == 5.0

    # all done
    return m


# main
if __name__ == "__main__":
    test()


# end of file
