#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Sanity check: a managed grid publishes its address and a cuda array interface that agree with
its buffer view, its sub-grids offset both correctly, and host-only grids have no interface
"""


def test():
    import numpy
    import pyre.grid

    # a managed grid
    g = pyre.grid.managed(shape=(3, 4), cell="float32")
    # its address is the one its buffer view sees
    assert g.address == numpy.asarray(g).ctypes.data

    # the cuda array interface describes the same cells
    cai = g.__cuda_array_interface__
    assert cai["version"] == 3
    assert cai["shape"] == (3, 4)
    assert cai["typestr"] == numpy.dtype(numpy.float32).str
    # with strides in bytes
    assert cai["strides"] == (16, 4)
    # at my address, writable
    assert cai["data"] == (g.address, False)

    # a sub-grid starts at its own first cell
    s = g[1:, 2:]
    assert s.address - g.address == (1 * 4 + 2) * 4
    assert s.__cuda_array_interface__["data"][0] == s.address

    # other cell types spell theirs the way numpy does
    for cell, dtype in [("int16", numpy.int16), ("uint64", numpy.uint64), ("complex128", numpy.complex128)]:
        m = pyre.grid.managed(shape=(2,), cell=cell)
        assert m.__cuda_array_interface__["typestr"] == numpy.dtype(dtype).str

    # host-only grids have an address but no cuda array interface
    h = pyre.grid.heap(shape=(2, 2), cell="float64")
    assert h.address == numpy.asarray(h).ctypes.data
    assert not hasattr(h, "__cuda_array_interface__")

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
