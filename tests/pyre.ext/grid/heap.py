#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Build heap grids through the single erased class and reach their cells through the buffer
    protocol
    """
    # the grid bindings
    from pyre.extensions.pyre import grid

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

    # a grid presents the python buffer protocol, which the builtin {memoryview} reads
    mv = memoryview(g)
    # matching geometry and cell type
    assert mv.ndim == 3
    assert tuple(mv.shape) == (2, 3, 4)
    assert mv.format == "d"
    # writable, since the storage is
    assert not mv.readonly

    # a write through one view is a write to the grid's memory, so a second view sees it
    mv[1, 2, 3] = 42.0
    mv[0, 0, 0] = 7.0
    other = memoryview(g)
    assert other[1, 2, 3] == 42.0
    assert other[0, 0, 0] == 7.0

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
        # view it through the buffer protocol
        v = memoryview(h)
        # the geometry comes through
        assert tuple(v.shape) == tuple(shape)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
