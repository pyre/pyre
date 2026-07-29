#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Exercise the read-only flavors of the map and view factories
    """
    # the grid bindings
    from pyre.extensions.pyre import grid

    # for a scratch path and its cleanup
    import os

    # a scratch data product
    uri = "grid_readonly_test.dat"
    # make sure a stale one is not lying around
    if os.path.exists(uri):
        os.remove(uri)

    # try, so the file is cleaned up no matter what
    try:
        # create a product and stamp a cell
        g = grid.map(uri=uri, shape=[2, 3], cell="float64")
        # through the buffer protocol
        memoryview(g)[1, 2] = 3.5
        # drop the grid, which unmaps and flushes the file
        del g

        # reopen the product for reading only
        r = grid.map(uri=uri, shape=[2, 3], cell="float64", create=False, writable=False)
        # the description says so
        assert r.writable is False
        # the stamped cell reads back, both through indexing
        assert r[1, 2] == 3.5
        # and through the buffer protocol, whose view is marked read-only
        mv = memoryview(r)
        assert mv.readonly is True
        assert mv[1, 2] == 3.5

        # writes through indexing are refused
        try:
            # this grid is read-only
            r[0, 0] = 1.0
            # so we should not get here
            assert False
        except ValueError:
            # as expected
            pass
        # and so are writes through the buffer
        try:
            # the view is read-only
            mv[0, 0] = 1.0
            # so we should not get here
            assert False
        except TypeError:
            # as expected
            pass
        # let go of the mapping
        del r, mv

        # a fresh product that could never be filled is a caller mistake
        try:
            # ask for a read-only product that does not exist yet
            grid.map(uri="nonsense.dat", shape=[2, 3], cell="float64", writable=False)
            # so we should not get here
            assert False
        except ValueError:
            # as expected
            pass
    # no matter what happened
    finally:
        # clean up the scratch product
        if os.path.exists(uri):
            os.remove(uri)

    # a read-only source exports its buffer for reading only; {bytes} is the canonical case
    source = bytes(memoryview(b"\x01\x02\x03\x04\x05\x06"))
    # asking for a writable view of it is refused by the exporter
    try:
        # {bytes} refuses write access
        grid.view(source=source, shape=[2, 3], cell="int8")
        # so we should not get here
        assert False
    except BufferError:
        # as expected
        pass
    # but a read-only view lays a grid over it with no copy
    v = grid.view(source=source, shape=[2, 3], cell="int8", writable=False)
    # the description says so
    assert v.writable is False
    # and the cells read back
    assert v[0, 0] == 1
    assert v[1, 2] == 6
    # while writes are refused
    try:
        # this grid is read-only
        v[0, 0] = 9
        # so we should not get here
        assert False
    except ValueError:
        # as expected
        pass

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
