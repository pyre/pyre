#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the bound {Matrix.swapRows} directly, through the extension rather than the {gsl.matrix}
shim, so a failure isolates the c++ layer
"""


def test():
    # the bindings
    from gsl import libgsl

    # an asymmetric matrix, so a swap of rows cannot be confused with a swap of columns
    m = libgsl.Matrix(shape=(3, 4))
    for row in range(3):
        for column in range(4):
            m.set((row, column), float(row * 4 + column))

    # swap the first row with the last, naming the last with a reflected negative index
    m.swapRows(0, -1)

    # the last row's cells now sit in the first, and the first row's in the last
    assert m.get((0, 1)) == 9.0 and m.get((2, 1)) == 1.0
    # the middle row is untouched
    assert m.get((1, 1)) == 5.0

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
