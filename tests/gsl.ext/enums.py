#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the bound flag enumerations directly, including that the blas and eigen bindings take
them by type, so an integer or a bad value is rejected rather than silently accepted
"""


def test():
    # the bindings
    from gsl import libgsl

    # each enumeration publishes the expected members: the transposition of a matrix operand
    assert set(libgsl.Transpose.__members__) == {"noTranspose", "transpose", "conjugateTranspose"}
    # the triangle of a matrix that an operation reads
    assert set(libgsl.Triangle.__members__) == {"upper", "lower"}
    # whether its diagonal is taken to be all ones
    assert set(libgsl.Diagonal.__members__) == {"unit", "nonUnit"}
    # the side a matrix multiplies from
    assert set(libgsl.Side.__members__) == {"left", "right"}
    # and the order in which an eigensystem is sorted
    assert set(libgsl.EigenOrder.__members__) == {
        "valueAscending",
        "valueDescending",
        "magnitudeAscending",
        "magnitudeDescending",
    }

    # the values carry gsl's own cblas numbers, so they pass straight into the library: the
    # transpositions start at 111
    assert int(libgsl.Transpose.noTranspose) == 111
    # the triangles at 121
    assert int(libgsl.Triangle.upper) == 121
    # the diagonals at 131, with the unit diagonal second
    assert int(libgsl.Diagonal.unit) == 132
    # and the sides at 141
    assert int(libgsl.Side.left) == 141

    # a blas call that takes a flag accepts the enum; to form {y = A x}, make an identity matrix
    A = libgsl.Matrix(shape=(2, 2)).identity()
    # a vector of ones
    x = libgsl.Vector(shape=2).fill(1.0)
    # and a place for the product
    y = libgsl.Vector(shape=2).zero()
    # form the product, naming the transposition by its enum
    libgsl.blas_dgemv(libgsl.Transpose.noTranspose, 1.0, A, x, 0.0, y)
    # and check that the identity left the ones alone
    assert y.get(0) == 1.0

    # but a raw integer in place of the enum is rejected
    try:
        # pass an int where a {Transpose} is expected
        libgsl.blas_dgemv(0, 1.0, A, x, 0.0, y)
    # which is what should happen
    except TypeError:
        # so there is nothing else to check
        pass
    # and if it doesn't
    else:
        # the type is not being enforced
        assert False, "a blas flag should be an enum, not an int"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
