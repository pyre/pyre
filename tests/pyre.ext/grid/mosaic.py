#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Exercise the out-of-core workflow: describe a mosaic for free, find the tiles a window
    touches, and reach the cells through zero-copy panes
    """
    # the grid bindings
    from pyre.extensions.pyre import grid

    # describe a product diced into a hundred tiles; nothing is allocated yet
    m = grid.mosaic(shape=[100, 100], tile=[10, 10], cell="float64")

    # the metadata reflects the description
    assert m.rank == 2
    assert m.shape == [100, 100]
    assert m.origin == [0, 0]
    assert m.tileShape == [10, 10]
    assert m.tiles == [10, 10]
    # the storage bill is every tile at full size
    assert m.cells == 100 * 100
    # the cell type survives the trip
    assert m.cell == "float64"
    # and describing the product allocated nothing
    assert m.residents == 0

    # an algorithm's working window, deliberately not aligned with the tiles
    touched = m.tilesOverlapping(base=[35, 42], shape=[20, 20])
    # the window leans into the tiles at {3,4} and spills over into a 3x3 block of them
    assert touched == [[3, 4], [3, 5], [3, 6], [4, 4], [4, 5], [4, 6], [5, 4], [5, 5], [5, 6]]

    # an index falls in the tile that covers it
    assert m.tileOf(index=[35, 42]) == [3, 4]

    # nothing is resident until a pane is asked for
    assert m.resident(tile=[3, 4]) is False
    # touch the working set
    for t in touched:
        # ask for the pane over each touched tile
        p = m.pane(tile=t)
        # each one is an ordinary grid over exactly one tile
        assert p.shape == [10, 10]
        # backed by the tile's own page
        assert p.strategy == "pane"
        # and writable, since the mosaic is
        assert p.writable is True
    # the working set is now resident: nine pages, nothing more
    assert m.residents == 9
    # and the page state reflects the touch
    assert m.resident(tile=[3, 4]) is True
    # but no content has been declared meaningful yet
    assert m.valid(tile=[3, 4]) is False

    # fill one tile through its pane, the way a reader pulling chunks from a file would
    t = [4, 5]
    # get the pane
    p = m.pane(tile=t)
    # a pane speaks the buffer protocol, so its cells are reachable with no copy
    mv = memoryview(p)
    # stamp every cell
    for i in range(10):
        # sweeping the tile's own box
        for j in range(10):
            # with a recognizable value
            mv[i, j] = 45.0
    # declare the deposit, mirroring the c++ discipline
    m.validate(tile=t)
    m.taint(tile=t)
    # the state reflects the declarations
    assert m.valid(tile=t) is True
    assert m.clean(tile=t) is False
    # saving the page marks it clean again
    m.flush(tile=t)
    assert m.clean(tile=t) is True

    # a fresh pane over the same tile addresses the same page, so the writes are there
    q = m.pane(tile=t)
    # check a cell through the new pane's own view
    assert memoryview(q)[0, 0] == 45.0
    # and single cell access through the pane sees the same memory
    assert q[9, 9] == 45.0

    # writes through a pane's indexing land in the page too
    q[0, 0] = 7.0
    # visible through the first pane, since there is only one page
    assert mv[0, 0] == 7.0

    # a pane must keep the store alive after the mosaic object itself is gone
    del m, p, q
    # the collector, so we can force the issue
    import gc

    # sweep
    gc.collect()
    # the surviving view still reads the page
    assert mv[0, 0] == 7.0

    # single cell access goes through the mosaic itself, no pane required
    m = grid.mosaic(shape=[4, 6], tile=[2, 3], cell="int32")
    # a write materializes the page that holds the cell
    m[3, 4] = 13
    # this cell falls in tile {1,1}, whose page is now the only resident one
    assert m.residents == 1
    assert m.resident(tile=[1, 1]) is True
    # and the write tainted it, since the divergence is visible to the binding
    assert m.clean(tile=[1, 1]) is False
    # the cell reads straight back
    assert m[3, 4] == 13
    # a negative coordinate counts from the end of its axis
    assert m[-1, -2] == 13
    # the pane over the tile addresses the same page, at the cell's tile-local coordinates
    assert memoryview(m.pane(tile=[1, 1]))[1, 1] == 13

    # reading a cell whose page was never brought in is refused
    try:
        # this cell falls in tile {0,0}, which is not resident
        m[0, 0]
        # so we should not get here
        assert False
    except ValueError:
        # as expected
        pass

    # out of range indices are rejected
    try:
        # too large
        m[4, 0]
        # so we should not get here
        assert False
    except IndexError:
        # as expected
        pass
    # and so are indices of the wrong arity
    try:
        # one coordinate short
        m[1]
        # so we should not get here
        assert False
    except IndexError:
        # as expected
        pass

    # out of range tiles are rejected
    try:
        # this tile does not exist
        m.pane(tile=[2, 2])
        # so we should not get here
        assert False
    except IndexError:
        # as expected
        pass
    # and so are windows that reach outside the box
    try:
        # this box leaks out of the mosaic
        m.tilesOverlapping(base=[2, 4], shape=[10, 10])
        # so we should not get here
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
