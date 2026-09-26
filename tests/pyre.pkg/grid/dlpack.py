#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A grid hands out the dlpack capsule its consumer asks for: the versioned kind to those that
request dlpack 1.0 or later, and the legacy kind to those that don't ask
"""


def test():
    import ctypes
    import numpy
    import pyre.grid

    # read the name of a capsule
    name = ctypes.pythonapi.PyCapsule_GetName
    name.restype = ctypes.c_char_p
    name.argtypes = [ctypes.py_object]

    # a heap grid
    g = pyre.grid.heap(shape=(2, 3), cell="float64")

    # a consumer that doesn't ask for a version gets the legacy capsule
    assert name(g.__dlpack__()) == b"dltensor"
    assert name(g.__dlpack__(max_version=None)) == b"dltensor"
    # as does one that asks for a version before 1.0
    assert name(g.__dlpack__(max_version=(0, 8))) == b"dltensor"
    # while one that asks for 1.0 or later gets the versioned capsule
    assert name(g.__dlpack__(max_version=(1, 0))) == b"dltensor_versioned"
    assert name(g.__dlpack__(max_version=(1, 3))) == b"dltensor_versioned"

    # numpy imports it with no copy
    numpy.asarray(g)[...] = numpy.arange(6).reshape(2, 3)
    a = numpy.from_dlpack(g)
    assert a.ctypes.data == g.address
    assert (a == numpy.arange(6).reshape(2, 3)).all()

    # capsules nobody imports clean up after themselves, in both flavors
    for _ in range(100):
        g.__dlpack__()
        g.__dlpack__(max_version=(1, 0))

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
