#!/usr/bin/env python3
# -*- python -*-
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
    # go through its rows
    for row in range(3):
        # and its columns
        for column in range(4):
            # and number the cells in row major order
            m[row, column] = row * 4 + column

    # a negative coordinate counts from the end, on either axis: the last cell
    assert m[-1, -1] == m[2, 3]
    # and the first
    assert m[-3, -4] == m[0, 0]

    # reading past the last row raises, through the subscript
    assert raises(lambda: m[3, 0])
    # and so does reading past the last column
    assert raises(lambda: m[0, 4])
    # writing past the last row
    assert raises(lambda: m.__setitem__((3, 0), 1.0))
    # or past the last column
    assert raises(lambda: m.__setitem__((0, 4), 1.0))

    # a too-negative row raises rather than reflecting to a still-negative slot
    assert raises(lambda: m[-4, 0])
    # and so does a too-negative column
    assert raises(lambda: m[0, -5])

    # the row and column accessors check their index; these return a fresh vector of the right
    # length, so an out of range row raises
    assert raises(lambda: m.getRow(3))
    # and so does an out of range column
    assert raises(lambda: m.getColumn(4))
    # the setters check the same way, for rows
    assert raises(lambda: m.setRow(3, gsl.vector(shape=4)))
    # and for columns
    assert raises(lambda: m.setColumn(4, gsl.vector(shape=3)))

    # a too-negative row index raises rather than reflecting to a still-negative slot
    assert raises(lambda: m.getRow(-4))
    # and so does a too-negative column index
    assert raises(lambda: m.getColumn(-5))

    # the row and column swaps check both of their indices, on the axis they act along: the
    # second row
    assert raises(lambda: m.swapRows(0, 3))
    # the first row
    assert raises(lambda: m.swapRows(3, 0))
    # the second column
    assert raises(lambda: m.swapColumns(0, 4))
    # and the first column
    assert raises(lambda: m.swapColumns(4, 0))
    # a too-negative row raises rather than reflecting to a still-negative slot
    assert raises(lambda: m.swapRows(0, -4))
    # and so does a too-negative column
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
