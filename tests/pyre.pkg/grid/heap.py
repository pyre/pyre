#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Make a heap grid through the package and reach its cells through the buffer protocol
"""


def test():
    # the grid package
    import pyre.grid

    # make a grid over a fresh block of heap memory
    g = pyre.grid.heap(shape=(2, 3, 4), dtype="float64")
    # it is an instance of the published grid class
    assert isinstance(g, pyre.grid.grid)
    # with the geometry we asked for
    assert g.rank == 3
    assert g.shape == [2, 3, 4]

    # view it through the builtin buffer protocol
    mv = memoryview(g)
    # the view has the grid's shape and cell type
    assert tuple(mv.shape) == (2, 3, 4)
    assert mv.format == "d"

    # a write through the view lands in the grid's memory, so a fresh view sees it
    mv[1, 2, 3] = 17.0
    assert memoryview(g)[1, 2, 3] == 17.0

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
