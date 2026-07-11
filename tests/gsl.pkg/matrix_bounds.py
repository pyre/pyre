#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that indices crossing into a matrix are reflected and bounds-checked, so out of range
access raises {IndexError} rather than leaning on gsl's optional range check
"""


def raises(fn):
    """
    Return True if calling {fn} raises {IndexError}
    """
    # try the call
    try:
        # which is expected to fail
        fn()
    # if it raises the right thing
    except IndexError:
        # good
        return True
    # otherwise it did not guard
    return False


def test():
    # get the package
    import gsl

    # a matrix with a known pattern
    m = gsl.matrix(shape=(3, 4))
    for row in range(3):
        for column in range(4):
            m[row, column] = row * 4 + column

    # a negative coordinate counts from the end, on either axis
    assert m[-1, -1] == m[2, 3]
    assert m[-3, -4] == m[0, 0]

    # reading or writing past either edge raises, through the subscript
    assert raises(lambda: m[3, 0])
    assert raises(lambda: m[0, 4])
    assert raises(lambda: m.__setitem__((3, 0), 1.0))
    assert raises(lambda: m.__setitem__((0, 4), 1.0))

    # a too-negative coordinate raises rather than reflecting to a still-negative slot
    assert raises(lambda: m[-4, 0])
    assert raises(lambda: m[0, -5])

    # the row and column accessors check their index; these return a fresh vector of the right
    # length, so an out of range row or column raises
    assert raises(lambda: m.getRow(3))
    assert raises(lambda: m.getColumn(4))
    assert raises(lambda: m.setRow(3, gsl.vector(shape=4)))
    assert raises(lambda: m.setColumn(4, gsl.vector(shape=3)))

    # a too-negative row or column index raises rather than reflecting to a still-negative slot
    assert raises(lambda: m.getRow(-4))
    assert raises(lambda: m.getColumn(-5))

    # the row and column swaps check both of their indices, on the axis they act along
    assert raises(lambda: m.swapRows(0, 3))
    assert raises(lambda: m.swapRows(3, 0))
    assert raises(lambda: m.swapColumns(0, 4))
    assert raises(lambda: m.swapColumns(4, 0))
    # and a too-negative index raises rather than reflecting to a still-negative slot
    assert raises(lambda: m.swapRows(0, -4))
    assert raises(lambda: m.swapColumns(0, -5))

    # a reflected row index reaches the last row
    assert m.getRow(-1)[0] == m[2, 0]
    # and a reflected column index reaches the last column
    assert m.getColumn(-1)[0] == m[0, 3]

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
