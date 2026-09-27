#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A managed grid publishes its address, its dlpack device, and its cuda array interface
"""


def test():
    # support
    import numpy
    import pyre.cuda

    # a managed grid
    g = pyre.cuda.managed(shape=(3, 4), cell="float32")
    # its address is the one its buffer view sees
    assert g.address == numpy.asarray(g).ctypes.data
    # it lives in cuda managed memory, as dlpack spells it
    assert g.__dlpack_device__() == (13, 0)
    # its cuda array interface describes the same cells
    cai = g.__cuda_array_interface__
    assert cai["version"] == 3
    assert cai["shape"] == (3, 4)
    assert cai["typestr"] == numpy.dtype(numpy.float32).str
    # with strides in bytes
    assert cai["strides"] == (16, 4)
    # at its address, writable
    assert cai["data"] == (g.address, False)
    # and numpy imports it through dlpack without a copy
    assert numpy.from_dlpack(g).ctypes.data == g.address

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
