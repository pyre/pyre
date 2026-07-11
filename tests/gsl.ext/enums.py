#!/usr/bin/env python3
# -*- Python -*-
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

    # each enumeration publishes the expected members
    assert set(libgsl.Transpose.__members__) == {"noTranspose", "transpose", "conjugateTranspose"}
    assert set(libgsl.Triangle.__members__) == {"upper", "lower"}
    assert set(libgsl.Diagonal.__members__) == {"unit", "nonUnit"}
    assert set(libgsl.Side.__members__) == {"left", "right"}
    assert set(libgsl.EigenOrder.__members__) == {
        "valueAscending",
        "valueDescending",
        "magnitudeAscending",
        "magnitudeDescending",
    }

    # the values carry gsl's own cblas numbers, so they pass straight into the library
    assert int(libgsl.Transpose.noTranspose) == 111
    assert int(libgsl.Triangle.upper) == 121
    assert int(libgsl.Diagonal.unit) == 132
    assert int(libgsl.Side.left) == 141

    # a blas call that takes a flag accepts the enum
    A = libgsl.Matrix(shape=(2, 2)).identity()
    x = libgsl.Vector(shape=2).fill(1.0)
    y = libgsl.Vector(shape=2).zero()
    libgsl.blas_dgemv(libgsl.Transpose.noTranspose, 1.0, A, x, 0.0, y)
    assert y.get(0) == 1.0

    # but a raw integer in place of the enum is rejected
    try:
        # pass an int where a {Transpose} is expected
        libgsl.blas_dgemv(0, 1.0, A, x, 0.0, y)
    # which is what should happen
    except TypeError:
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
