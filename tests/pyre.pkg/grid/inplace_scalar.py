#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
In-place arithmetic between a heap grid and python numbers agrees with numpy
"""


def test():
    # support
    import numpy
    import pyre.grid

    # a grid of reals
    x = pyre.grid.heap(shape=(4,), cell="float32")
    # filled with known values
    numpy.asarray(x)[...] = [1, 2, 3, 4]
    # combined with integers and floats
    x += 1
    x *= 2.5
    x -= 0.5
    x /= 2
    # agrees with numpy
    assert (
        numpy.asarray(x) == (numpy.array([1, 2, 3, 4], dtype="float32") + 1) * 2.5 / 2 - 0.25
    ).all()

    # a grid of complex numbers
    z = pyre.grid.heap(shape=(2,), cell="complex128")
    # filled with known values
    numpy.asarray(z)[...] = [1 + 1j, 2 - 1j]
    # takes complex numbers
    z *= 1j
    # and agrees with numpy
    assert (numpy.asarray(z) == numpy.array([1 + 1j, 2 - 1j]) * 1j).all()

    # a grid of integers
    i = pyre.grid.heap(shape=(3,), cell="uint8")
    # filled with known values
    numpy.asarray(i)[...] = [250, 1, 2]
    # wraps around the way numpy's integers do
    i += 10
    assert numpy.asarray(i).tolist() == [4, 11, 12]

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
