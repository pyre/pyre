#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a raster shares the cells of the python buffer it is made over, keeps the buffer
alive, and feeds a slice that cuts tiles out of it
"""


def test():
    # support
    import gc

    # the bindings
    from pyre.extensions.pyre import flow, grid

    # a grid of complex values on the heap, which owns its cells
    cells = grid.heap(shape=[6, 8], cell="complex64")
    # each one says where it is
    for line in range(6):
        # one sample at a time
        for sample in range(8):
            # the line in the real part, the sample in the imaginary one
            cells[line, sample] = complex(line, sample)

    # a raster over them
    raster = flow.raster(source=cells, name="raster")
    # has their shape
    assert raster.shape == (6, 8)
    # and starts fresh, since its cells hold what they hold
    assert not raster.stale
    # and keeps them alive after python lets go of the grid
    del cells
    gc.collect()

    # find the slice of complex rasters in the catalog
    catalog = flow.catalog()
    (entry,) = [
        e
        for e in catalog.factories.values()
        if e.className == "Slice"
        and catalog.products[e.slots[0].product].cell == "std::complex<float>"
    ]
    # the raster is what its source slot takes
    assert entry.slots[0].accepts(raster)
    # make one
    slice = catalog.makeFactory(decl=entry.decl, name="slice")
    # and a tile of two lines and three samples
    tile = catalog.makeProduct(decl=entry.slots[1].product, name="tile", shape=(2, 3))
    # wire them
    assert slice.bind(slot="source", product=raster)
    assert slice.bind(slot="slice", product=tile)
    # start at the second line and sample, counted in strides, every other cell
    assert slice.set(setting="origin", value=(1, 1))
    assert slice.set(setting="stride", value=(2, 2))

    # pull the tile
    view = tile.read()
    # the cell at {row, column} is the one of the raster at {(1 + row) * 2, (1 + column) * 2}
    for row in range(2):
        # one column at a time
        for column in range(3):
            # check
            assert view[row, column] == complex(2 + 2 * row, 2 + 2 * column)

    # a buffer without two axes
    try:
        # makes no raster
        flow.raster(source=grid.heap(shape=[4], cell="complex64"), name="line")
        # so we can't get here
        assert False, "unreachable"
    # by raising
    except ValueError:
        # as expected
        pass
    # nor does a buffer of cells it does not support
    try:
        # such as bytes
        flow.raster(source=grid.heap(shape=[2, 2], cell="uint8"), name="bytes")
        # so we can't get here
        assert False, "unreachable"
    # by raising
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
