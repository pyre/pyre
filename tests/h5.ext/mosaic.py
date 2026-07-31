#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Exercise the h5-backed mosaic: produce a chunked product through one, and read it back
    through another
    """
    # get the bindings
    from pyre.extensions import libh5

    # for a scratch path and its cleanup
    import os

    # the recognizable content of the product
    def stamp(row, col):
        # a value that encodes its own coordinates
        return float(100 * row + col)

    # a scratch data product
    uri = "h5_ext_mosaic.h5"
    # make sure a stale one is not lying around
    if os.path.exists(uri):
        os.remove(uri)

    # make the file
    f = libh5.File(uri=uri, mode="w")
    # describe the extent
    space = libh5.DataSpace(shape=[100, 100])
    # and the chunking, deliberately not a divisor of the extent along either axis
    dcpl = libh5.properties.dcpl()
    dcpl.setChunk(shape=[30, 40])
    # make the dataset
    dataset = f.create(path="product", type=libh5.types.native.double, space=space, dcpl=dcpl)

    # the dataspaces agree on the extent across the wrapper boundary
    assert dataset.space.sameExtent(other=space)

    # the producer's mosaic, over the dataset's own chunking
    m = dataset.mosaic(cell="float64")
    # it is wired to its backing store
    assert m.connected is True
    # its geometry reflects the product
    assert m.shape == [100, 100]
    assert m.tileShape == [30, 40]
    assert m.tiles == [4, 3]
    # and nothing is resident yet
    assert m.residents == 0

    # the cells to stamp, spread across chunks, including the doubly clipped one
    probes = [(0, 0), (35, 45), (70, 85), (94, 94)]
    # deposit them; writes through indexing materialize the page and taint it
    for row, col in probes:
        m[row, col] = stamp(row, col)
    # push what diverged; the untouched chunks move nothing
    m.flush()

    # a consumer pulls one chunk at a time
    r = dataset.mosaic(cell="float64")
    # the chunk that holds a probe
    t = r.tileOf(index=[35, 45])
    # pull it
    r.fill(tile=t)
    # exactly one page came in
    assert r.residents == 1
    # and the cell holds its stamp
    assert r[35, 45] == stamp(35, 45)

    # an impatient consumer declares the smallest mosaic that covers its window
    w = dataset.mosaic(cell="float64", base=[70, 70], shape=[25, 25])
    # and asks for all of it
    w.fill()
    # the window touches a 2x2 block of chunks
    assert w.residents == 4
    # and reads back in the product's own index space
    assert w[70, 85] == stamp(70, 85)
    assert w[94, 94] == stamp(94, 94)

    # panes are ordinary grids over one page each: numpy-ready, zero-copy
    p = w.pane(tile=w.tileOf(index=[94, 94]))
    # the pane is a full chunk
    assert p.shape == [30, 40]
    # backed by the page
    assert p.strategy == "pane"
    # whose cells are reachable through the buffer protocol, at tile-local coordinates
    mv = memoryview(p)
    assert mv[94 - 90, 94 - 80] == stamp(94, 94)

    # the update loop: pull, modify, declare, push
    t = r.tileOf(index=[35, 45])
    # the page is already resident; change the cell
    r[35, 45] = 999.0
    # writes through indexing taint on their own, so just push
    r.flush()
    # a fresh reader sees the change
    v = dataset.mosaic(cell="float64")
    v.fill(tile=t)
    assert v[35, 45] == 999.0
    # and its neighbor chunk is untouched
    v.fill(tile=v.tileOf(index=[94, 94]))
    assert v[94, 94] == stamp(94, 94)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
