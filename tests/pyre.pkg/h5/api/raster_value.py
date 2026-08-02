#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the value model for array datasets: their values are raster handles. A raster is
cheap to build and moves no data; it carries the hdf5 metadata a consumer needs in order to
choose an access strategy, and the factories that realize the choice: {mosaic} builds an
out-of-core view whose chunks move only when asked to, and {tile} materializes a dense
private grid on the heap. A producer writes a chunked product through a mosaic, the pkg read
path hands the dataset value back as a raster, and the consumer exercises both strategies.
"""


def test():
    # support
    import pyre

    # the bindings are the engine here; if they are not present
    if pyre.libpyre is None:
        # there is nothing to exercise
        return
    # reach the low level hdf5 bindings
    libh5 = pyre.h5.libh5
    # same story
    if libh5 is None:
        # nothing to do
        return

    # the recognizable content of the product
    def stamp(row, col):
        # a value that encodes its own coordinates
        return float(100 * row + col)

    # place the test file
    uri = pyre.primitives.path("raster_value.h5")

    # the producer: write a chunked product through a mosaic
    # create the file and grab the low level handle, which doubles as the root group
    root = pyre.h5.api.file()._pyre_local(uri=uri, mode="w")._pyre_id
    # describe the extent
    space = libh5.DataSpace(shape=[100, 100])
    # and the chunking, deliberately not a divisor of the extent along either axis
    dcpl = libh5.properties.dcpl()
    dcpl.setChunk(shape=[30, 40])
    # lay down the dataset
    dataset = root.create(path="raster", type=libh5.types.native.double, space=space, dcpl=dcpl)
    # the producer's mosaic, wired to the file
    m = dataset.mosaic(cell="float64")
    # the cells to stamp, spread across chunks, including the doubly clipped one
    probes = [(0, 0), (35, 45), (94, 94)]
    # deposit them; writes through indexing materialize the page and taint it
    for row, col in probes:
        m[row, col] = stamp(row, col)
    # make the file agree
    m.flush()
    # and let go of the handles, closing the file
    del m, dataset, root

    # the consumer: the pkg read path; {r+} so the update below can flow back
    product = pyre.h5.read(uri=uri, mode="r+")
    # member access auto-dereferences datasets to their value: a raster handle
    value = product.raster
    # rasters are cheap: no payload moved; they answer the questions that inform the
    # choice of access strategy, starting with the geometry
    assert value.shape == [100, 100]
    assert value.rank == 2
    # the on-disk layout: this product is chunked, with the producer's tiling
    assert value.layout == libh5.Layout.chunked
    assert value.chunk == [30, 40]
    # no filters were applied
    assert list(value.filters) == []
    # the in-memory type is interrogable, down to its grid cell name
    assert value.memtype.cell == "float64"
    # so is the on-disk type: a bound datatype proxy with its class and precision
    assert value.disktype.cell == libh5.DataSetType.float
    assert value.disktype.bytes == 8

    # the out-of-core strategy: a mosaic over the product's own chunking
    m = value.mosaic()
    # wired to the file
    assert m.connected is True
    # with the product's geometry
    assert m.shape == [100, 100]
    assert m.tileShape == [30, 40]
    # and nothing resident: building the view moved no payload
    assert m.residents == 0
    # pull only the chunks that hold the probes
    for row, col in probes:
        # each one materializes on demand
        m.fill(tile=m.tileOf(index=[row, col]))
    # the stamps came through
    for row, col in probes:
        assert m[row, col] == stamp(row, col)
    # update the product in place: writes through indexing declare for themselves
    m[35, 45] = 999.0
    # push what diverged
    m.flush()

    # the dense strategy: a private tile on the heap over a window of interest
    tile = value.tile(origin=[30, 40], shape=[10, 10])
    # tile indices are window-local: the caller keeps track of where they placed it;
    # the update above lands at [5, 5]
    assert tile[5, 5] == 999.0
    # the tile is a private copy: scribbling on it does not touch the file
    tile[0, 0] = 137.0

    # a fresh read sees the mosaic update
    fresh = pyre.h5.read(uri=uri)
    # get the raster
    check = fresh.raster
    # build an out-of-core view
    c = check.mosaic()
    # pull the chunk that received the update
    c.fill(tile=c.tileOf(index=[35, 45]))
    # the update persisted
    assert c[35, 45] == 999.0
    # the tile scribble did not: its target cell still holds the fill value
    assert c[30, 40] == 0.0
    # pull a neighboring chunk as well
    c.fill(tile=c.tileOf(index=[94, 94]))
    # it is undisturbed
    assert c[94, 94] == stamp(94, 94)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
