#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Create a file-backed grid and confirm its cells survive being written, closed, and reopened
    """
    # the grid bindings
    from pyre.extensions.pyre import grid
    # for a scratch path and its cleanup
    import os

    # a scratch data product
    uri = "grid_map_test.dat"
    # make sure a stale one is not lying around
    if os.path.exists(uri):
        os.remove(uri)

    # try, so the file is cleaned up no matter what
    try:
        # create a file-backed grid
        g = grid.map(uri=uri, shape=[2, 3, 4], dtype="float64")
        # it reports the geometry we asked for
        assert g.shape == [2, 3, 4]
        # and knows it is file backed
        assert g.strategy == "map"

        # write a recognizable value through the buffer protocol
        memoryview(g)[1, 2, 3] = 3.5
        # drop the grid, which unmaps and flushes the file
        del g

        # map the same file again over the same shape, opening the existing product
        h = grid.map(uri=uri, shape=[2, 3, 4], dtype="float64", create=False)
        # the value must have persisted to disk
        assert memoryview(h)[1, 2, 3] == 3.5
        # let go of the second mapping
        del h

    # in all cases
    finally:
        # remove the scratch file
        if os.path.exists(uri):
            os.remove(uri)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
