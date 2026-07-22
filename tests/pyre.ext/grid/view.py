#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Lay a grid over memory python already holds, and confirm it aliases that memory
    """
    # the grid bindings
    from pyre.extensions.pyre import grid
    # the standard array module gives us a block of typed memory with no third party support
    import array

    # a flat block of twenty four doubles, all zero
    source = array.array("d", [0.0] * 24)

    # lay a grid over it, without copying
    g = grid.view(source=source, shape=[2, 3, 4], dtype="float64")
    # it reports the geometry we asked for
    assert g.shape == [2, 3, 4]
    # and knows it does not own its cells
    assert g.strategy == "view"

    # a write through the grid is a write to the source block
    memoryview(g)[1, 2, 3] = 9.0
    # so the original array sees it: cell {1,2,3} of a {2,3,4} c-order grid is flat index 23
    assert source[23] == 9.0

    # and a write to the source block is a read through the grid
    source[0] = 4.0
    assert memoryview(g)[0, 0, 0] == 4.0

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
