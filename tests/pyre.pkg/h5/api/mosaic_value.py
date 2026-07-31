#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the out-of-core value model: array dataset values are mosaics wired to their file.
A producer writes a chunked product through a mosaic, the pkg read path hands the dataset
value back as one, the consumer fills only the chunks it touches, and updates flow back to
the file through {flush}.
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
    uri = pyre.primitives.path("mosaic_value.h5")

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
    # member access auto-dereferences datasets to their value: an out-of-core mosaic
    value = product.raster
    # wired to the file
    assert value.connected is True
    # with the product's geometry
    assert value.shape == [100, 100]
    assert value.tileShape == [30, 40]
    # and nothing resident: reading the structure of the product moved no payload
    assert value.residents == 0

    # pull only the chunks that hold the probes
    for row, col in probes:
        # each one materializes on demand
        value.fill(tile=value.tileOf(index=[row, col]))
    # the stamps came through
    for row, col in probes:
        assert value[row, col] == stamp(row, col)

    # update the product in place: writes through indexing declare for themselves
    value[35, 45] = 999.0
    # push what diverged
    value.flush()

    # a fresh read sees the update
    fresh = pyre.h5.read(uri=uri)
    # get the value
    check = fresh.raster
    # pull the chunk in question
    check.fill(tile=check.tileOf(index=[35, 45]))
    # the update persisted
    assert check[35, 45] == 999.0
    # pull a neighboring chunk as well
    check.fill(tile=check.tileOf(index=[94, 94]))
    # it is undisturbed
    assert check[94, 94] == stamp(94, 94)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
