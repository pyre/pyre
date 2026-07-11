#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the bound {Matrix} directly, through the extension rather than the {gsl.matrix} shim,
so a failure isolates the c++ layer
"""


def raises(fn, kind):
    """
    Return True if calling {fn} raises {kind}
    """
    # try the call
    try:
        # which is expected to fail
        fn()
    # if it raises the right thing
    except kind:
        # good
        return True
    # otherwise it did not guard
    return False


def test():
    # the bindings
    from gsl import libgsl

    # allocation and shape
    m = libgsl.Matrix(shape=(3, 4))
    assert m.shape == (3, 4)

    # the index is a {row, column} pair
    m.fill(0.0)
    m.set((1, 2), 7.0)
    assert m.get((1, 2)) == 7.0

    # a negative coordinate reflects to the mirrored cell, each axis using its own extent, so a
    # transposed reflection lands elsewhere; out of range and too-negative raise
    assert m.get((-2, -2)) == 7.0
    assert raises(lambda: m.get((3, 0)), IndexError)
    assert raises(lambda: m.get((0, 4)), IndexError)
    assert raises(lambda: m.set((3, 0), 1.0), IndexError)
    assert raises(lambda: m.get((-4, 0)), IndexError)

    # zero, identity, and copy
    m.identity()
    assert m.get((0, 0)) == 1.0 and m.get((0, 1)) == 0.0
    other = libgsl.Matrix(shape=(3, 4)).fill(5.0)
    m.copy(other)
    assert m.equal(other)

    # a known pattern for the rest
    for row in range(3):
        for column in range(4):
            m.set((row, column), float(row * 4 + column))

    # the cells as a tuple of rows
    assert m.tuple()[1] == (4.0, 5.0, 6.0, 7.0)

    # containment and extrema
    assert m.contains(6.0)
    assert m.max() == 11.0 and m.min() == 0.0
    assert m.minmax() == (0.0, 11.0)

    # the row and column fill methods take a caller-supplied vector
    row = libgsl.Vector(shape=4)
    m.getRow(1, row)
    assert row.get(0) == 4.0 and row.get(3) == 7.0
    column = libgsl.Vector(shape=3)
    m.getColumn(2, column)
    assert column.get(0) == 2.0 and column.get(2) == 10.0

    # and they bounds-check their index, reflecting a negative one
    assert raises(lambda: m.getRow(3, row), IndexError)
    assert raises(lambda: m.getColumn(4, column), IndexError)
    m.getRow(-1, row)
    assert row.get(0) == 8.0

    # setting a row from a vector
    m.setRow(0, libgsl.Vector(shape=4).fill(-1.0))
    assert m.get((0, 0)) == -1.0
    assert raises(lambda: m.setRow(3, row), IndexError)

    # elementwise arithmetic, in place
    a = libgsl.Matrix(shape=(2, 2)).fill(2.0)
    a.add(libgsl.Matrix(shape=(2, 2)).fill(3.0))
    assert a.get((0, 0)) == 5.0
    a.scale(2.0)
    assert a.get((0, 0)) == 10.0

    # transpose into a destination, leaving me untouched
    src = libgsl.Matrix(shape=(2, 3))
    for i in range(2):
        for j in range(3):
            src.set((i, j), float(i * 3 + j))
    dst = libgsl.Matrix(shape=(3, 2))
    src.transpose(dst)
    # every cell, so a row/column swap in the transpose is caught
    assert all(dst.get((j, i)) == src.get((i, j)) for i in range(2) for j in range(3))

    # the symmetric eigenproblem, filling caller-supplied storage in the requested order; a non
    # diagonal matrix is used so the off diagonal actually feeds the solver
    s = libgsl.Matrix(shape=(2, 2))
    s.set((0, 0), 2.0)
    s.set((0, 1), 1.0)
    s.set((1, 0), 1.0)
    s.set((1, 1), 2.0)
    values = libgsl.Vector(shape=2)
    vectors = libgsl.Matrix(shape=(2, 2))
    s.eigenSymmetric(libgsl.EigenOrder.valueAscending, values, vectors)
    # the eigenvalues of [[2,1],[1,2]] are 1 and 3
    assert abs(values.get(0) - 1.0) < 1e-12 and abs(values.get(1) - 3.0) < 1e-12

    # the buffer protocol hands numpy a zero-copy, correctly-strided view
    import numpy

    grid = numpy.asarray(m)
    assert grid.shape == (3, 4)
    # the layout is row major and untransposed; the asymmetric pattern catches a swapped stride
    assert all(grid[row, column] == m.get((row, column)) for row in range(3) for column in range(4))

    # a view is built through the view constructor and shares its parent's storage; the raw
    # binding has no python-level {view} method, that lives in the shim
    sub = libgsl.Matrix(m, (0, 1), (3, 2))
    sub.set((0, 0), 99.0)
    assert m.get((0, 1)) == 99.0

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
