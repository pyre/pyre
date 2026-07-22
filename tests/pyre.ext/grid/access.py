#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Reach a grid's cells with {g[i, j]} indexing, and confirm that writes land in the same memory
    the buffer protocol exposes
    """
    # the grid bindings
    from pyre.extensions.pyre import grid

    # make a two dimensional grid of doubles on the heap
    g = grid.heap(shape=[2, 3], cell="float64")

    # heap storage comes uninitialized, so stamp every cell with a known value before reading it
    for i in range(2):
        # over the second axis too
        for j in range(3):
            # lay down a definite zero
            g[i, j] = 0.0
    # now the grid reads back as the zeros we wrote
    assert g[0, 0] == 0.0
    assert g[1, 2] == 0.0

    # a write through the index is a write to the grid's memory, so the buffer protocol sees it
    g[1, 2] = 42.0
    g[0, 0] = 7.0
    # read it straight back through the index
    assert g[1, 2] == 42.0
    assert g[0, 0] == 7.0
    # and the very same cells through a memoryview, proving they share one block
    mv = memoryview(g)
    assert mv[1, 2] == 42.0
    assert mv[0, 0] == 7.0

    # the traffic runs the other way too: a write through the buffer is visible through the index
    mv[0, 1] = 3.5
    assert g[0, 1] == 3.5

    # a negative coordinate counts from the end of its axis
    g[-1, -1] = 9.0
    assert g[1, 2] == 9.0

    # out of range indices are rejected
    try:
        # too large
        g[2, 0]
        # should not get here
        assert False
    except IndexError:
        # as expected
        pass

    # complex cells make the round trip through python's own complex
    c = grid.heap(shape=[2, 2], cell="complex128")
    # write a complex value
    c[0, 1] = 2 - 3j
    # and read it back intact
    assert c[0, 1] == 2 - 3j

    # a partial index yields a sub-grid that shares the parent's cells
    row = g[0]
    # it has dropped the first axis
    assert row.rank == 1
    assert row.shape == [3]
    # and it reads the parent's row
    assert row[1] == 3.5
    # writing through the sub-grid writes to the parent's memory
    row[2] = 11.0
    assert g[0, 2] == 11.0

    # a slice keeps its axis and selects a strided run
    tail = g[1, 1:3]
    # one axis, two cells
    assert tail.rank == 1
    assert tail.shape == [2]
    # reading the tail of row 1: column 1 still holds its stamped zero, column 2 holds the 9.0
    assert tail[0] == 0.0
    assert tail[1] == 9.0

    # a full slice over both axes is the whole grid again, still sharing memory
    whole = g[:, :]
    assert whole.shape == [2, 3]
    whole[0, 0] = 5.0
    assert g[0, 0] == 5.0

    # assigning through a non-scalar index is refused; write the sub-grid's cells instead
    try:
        # a slice target
        g[0, :] = 1.0
        # should not get here
        assert False
    except IndexError:
        # as expected
        pass

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
