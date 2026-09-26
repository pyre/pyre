#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A dlpack consumer that asks for no version, or one before 1.0, gets the legacy capsule
"""


def test():
    # support
    import ctypes
    import pyre.grid

    # the function that reads the name of a capsule
    name = ctypes.pythonapi.PyCapsule_GetName
    # returns a string
    name.restype = ctypes.c_char_p
    # given the capsule
    name.argtypes = [ctypes.py_object]

    # make a grid
    g = pyre.grid.heap(shape=(2, 3), cell="float64")
    # a consumer that asks for no version gets the legacy capsule
    assert name(g.__dlpack__()) == b"dltensor"
    # as does one that says so explicitly
    assert name(g.__dlpack__(max_version=None)) == b"dltensor"
    # and one that asks for a version before 1.0
    assert name(g.__dlpack__(max_version=(0, 8))) == b"dltensor"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
