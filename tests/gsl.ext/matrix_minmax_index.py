#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the bound {Matrix.minIndex} and {Matrix.maxIndex} directly, through the extension rather
than the {gsl.matrix} shim, so a failure isolates the c++ layer
"""


def test():
    # the bindings
    from gsl import libgsl

    # an asymmetric matrix; the extrema sit at off-diagonal cells with distinct rows and columns,
    # so a transposed coordinate is caught
    m = libgsl.Matrix(shape=(3, 4))
    for row in range(3):
        for column in range(4):
            m.set((row, column), float(row * 4 + column))
    # the largest cell in the top right, the smallest in the bottom left
    m.set((0, 3), 99.0)
    m.set((2, 0), -7.0)

    # the largest cell is at {row 0, column 3}
    assert m.maxIndex() == (0, 3)
    # the smallest cell is at {row 2, column 0}
    assert m.minIndex() == (2, 0)

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
