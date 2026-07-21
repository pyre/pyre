#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Build heap grids through the single erased class and view them with numpy, with no copy
    """
    # the grid bindings
    from pyre.extensions.pyre import grid
    # numpy, which reads the buffer protocol
    import numpy

    # make a three dimensional grid of doubles on the heap
    g = grid.heap(shape=[2, 3, 4], dtype="float64")
    # it reports its own geometry
    assert g.rank == 3
    assert g.shape == [2, 3, 4]
    # canonically packed, so the trailing axis is contiguous
    assert g.strides == [12, 4, 1]
    # heap storage is writable
    assert g.writable
    # and it knows what backs it
    assert g.strategy == "heap"

    # numpy views the cells with no copy
    a = numpy.asarray(g)
    # matching shape and dtype
    assert a.shape == (2, 3, 4)
    assert a.dtype == numpy.dtype("float64")

    # a write through one view is a write to the grid's memory, so a second view sees it
    a[1, 2, 3] = 42.0
    a[0, 0, 0] = 7.0
    b = numpy.asarray(g)
    assert b[1, 2, 3] == 42.0
    assert b[0, 0, 0] == 7.0
    # which is only possible if both views share the grid's memory
    assert numpy.shares_memory(a, b)

    # one bound class serves every cell type and every rank; check a spread of them
    cases = {
        "int8": [5],
        "uint16": [2, 5],
        "int32": [2, 3, 4],
        "float32": [3, 3],
        "complex128": [2, 2, 2, 2],
    }
    # go through them
    for dtype, shape in cases.items():
        # build the grid
        h = grid.heap(shape=shape, dtype=dtype)
        # view it
        v = numpy.asarray(h)
        # the geometry and cell type come through
        assert list(v.shape) == shape
        assert v.dtype == numpy.dtype(dtype)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
