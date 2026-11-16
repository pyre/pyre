#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the bound {Matrix} directly, through the extension rather than the {gsl.matrix} shim,
so a failure isolates the c++ layer
"""


def raises(call, kind):
    """
    Return True if invoking {call} raises {kind}
    """
    # try the call
    try:
        # which is expected to fail
        call()
    # if it raises the right thing
    except kind:
        # good
        return True
    # otherwise it did not guard
    return False


def test():
    # the bindings
    from gsl import libgsl

    # make a matrix
    matrix = libgsl.Matrix(shape=(3, 4))
    # and check its shape
    assert matrix.shape == (3, 4)

    # clear it
    matrix.fill(0.0)
    # set a cell, indexed by a {row, column} pair
    matrix.set((1, 2), 7.0)
    # and read it back
    assert matrix.get((1, 2)) == 7.0

    # a negative coordinate reflects to the mirrored cell, each axis using its own extent, so a
    # transposed reflection lands elsewhere
    assert matrix.get((-2, -2)) == 7.0
    # rows past the end are refused
    assert raises(lambda: matrix.get((3, 0)), IndexError)
    # as are columns past the end
    assert raises(lambda: matrix.get((0, 4)), IndexError)
    # when writing as well
    assert raises(lambda: matrix.set((3, 0), 1.0), IndexError)
    # and so are negative coordinates that reach before the start
    assert raises(lambda: matrix.get((-4, 0)), IndexError)

    # make it the identity
    matrix.identity()
    # with ones on the diagonal and zeroes elsewhere
    assert matrix.get((0, 0)) == 1.0 and matrix.get((0, 1)) == 0.0
    # make another matrix
    other = libgsl.Matrix(shape=(3, 4)).fill(5.0)
    # copy it into mine
    matrix.copy(other)
    # after which the two are equal
    assert matrix.equal(other)

    # a known pattern for the rest
    for row in range(3):
        # one row at a time
        for column in range(4):
            # one cell at a time
            matrix.set((row, column), float(row * 4 + column))

    # the cells as a tuple of rows
    assert matrix.tuple()[1] == (4.0, 5.0, 6.0, 7.0)

    # the matrix contains the values of the pattern
    assert matrix.contains(6.0)
    # whose extrema are known
    assert matrix.max() == 11.0 and matrix.min() == 0.0
    # and are also reported together
    assert matrix.minmax() == (0.0, 11.0)

    # the row and column fill methods take a caller-supplied vector
    rowVector = libgsl.Vector(shape=4)
    # copy out a row
    matrix.getRow(1, rowVector)
    # and check its ends
    assert rowVector.get(0) == 4.0 and rowVector.get(3) == 7.0
    # similarly for a column
    columnVector = libgsl.Vector(shape=3)
    # copy it out
    matrix.getColumn(2, columnVector)
    # and check its ends
    assert columnVector.get(0) == 2.0 and columnVector.get(2) == 10.0

    # rows past the end are refused
    assert raises(lambda: matrix.getRow(3, rowVector), IndexError)
    # as are columns past the end
    assert raises(lambda: matrix.getColumn(4, columnVector), IndexError)
    # and a negative row counts from the end
    matrix.getRow(-1, rowVector)
    # so the last row starts at 8
    assert rowVector.get(0) == 8.0

    # set a row from a vector
    matrix.setRow(0, libgsl.Vector(shape=4).fill(-1.0))
    # and check
    assert matrix.get((0, 0)) == -1.0
    # rows past the end are refused here too
    assert raises(lambda: matrix.setRow(3, rowVector), IndexError)

    # elementwise arithmetic, in place
    total = libgsl.Matrix(shape=(2, 2)).fill(2.0)
    # add another matrix
    total.add(libgsl.Matrix(shape=(2, 2)).fill(3.0))
    # and check
    assert total.get((0, 0)) == 5.0
    # scale it
    total.scale(2.0)
    # and check
    assert total.get((0, 0)) == 10.0

    # transpose into a destination, leaving me untouched
    source = libgsl.Matrix(shape=(2, 3))
    # fill the source with a pattern that tells every cell apart
    for row in range(2):
        # one row at a time
        for column in range(3):
            # one cell at a time
            source.set((row, column), float(row * 3 + column))
    # make room for the transpose
    destination = libgsl.Matrix(shape=(3, 2))
    # the answer is the destination itself
    assert source.transpose(destination) is destination
    # every cell, so a row/column swap in the transpose is caught
    assert all(
        destination.get((column, row)) == source.get((row, column))
        for row in range(2)
        for column in range(3)
    )

    # transpose a square matrix in place
    square = libgsl.Matrix(shape=(2, 2)).fill(0.0)
    # with a single cell set off the diagonal
    square.set((0, 1), 1.0)
    # which hands me back
    assert square.transpose() is square
    # with the cell moved across the diagonal
    assert square.get((1, 0)) == 1.0 and square.get((0, 1)) == 0.0

    # the symmetric eigenproblem, filling caller-supplied storage in the requested order; a non
    # diagonal matrix is used so the off diagonal actually feeds the solver
    symmetric = libgsl.Matrix(shape=(2, 2))
    # the diagonal
    symmetric.set((0, 0), 2.0)
    # the cell above the diagonal
    symmetric.set((0, 1), 1.0)
    # and its mirror below it
    symmetric.set((1, 0), 1.0)
    # and the rest of the diagonal
    symmetric.set((1, 1), 2.0)
    # room for the eigenvalues
    values = libgsl.Vector(shape=2)
    # and the eigenvectors
    vectors = libgsl.Matrix(shape=(2, 2))
    # solve
    symmetric.eigenSymmetric(libgsl.EigenOrder.valueAscending, values, vectors)
    # the eigenvalues of [[2,1],[1,2]] are 1 and 3
    assert abs(values.get(0) - 1.0) < 1e-12 and abs(values.get(1) - 3.0) < 1e-12

    # the buffer protocol hands numpy a zero-copy, correctly-strided view
    import numpy

    # so a numpy array over the matrix
    grid = numpy.asarray(matrix)
    # has the same shape
    assert grid.shape == (3, 4)
    # the layout is row major and untransposed; the asymmetric pattern catches a swapped stride
    assert all(
        grid[row, column] == matrix.get((row, column)) for row in range(3) for column in range(4)
    )

    # a view is built through the view constructor and shares its parent's storage
    view = libgsl.Matrix(matrix, (0, 1), (3, 2))
    # so writing through the view
    view.set((0, 0), 99.0)
    # changes the parent
    assert matrix.get((0, 1)) == 99.0

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
