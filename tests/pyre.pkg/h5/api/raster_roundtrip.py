#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Write a numeric raster to disk and read it back, exercising the whole C++/Python data path:
{memtype.grid} builds the in-memory buffer, {DataSet.write} pushes it through the buffer
protocol, and {DataSet.read} pulls it back. This is the runtime contract that the erased grid
bindings and the {py::buffer} dataset I/O have to honor together.
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
    # pick a numeric in-memory type
    memtype = pyre.h5.memtypes.double
    # fix the geometry of the raster
    shape = [2, 3]

    # place the test file
    uri = pyre.primitives.path("raster_roundtrip.h5")
    # create it for writing and grab the low level file handle, which doubles as the root group
    root = pyre.h5.api.file()._pyre_local(uri=uri, mode="w")._pyre_id

    # describe the on-disk layout
    space = libh5.DataSpace(shape=shape)
    # and lay down the dataset over my on-disk type
    dataset = root.create(path="raster", type=memtype.htype, space=space)

    # build the source buffer over a fresh block of heap memory of my cell type
    src = memtype.grid(shape=shape)
    # view it through the buffer protocol
    srcview = memoryview(src)
    # the geometry has to come through untouched
    assert tuple(srcview.shape) == tuple(shape)
    # fill every cell with a distinct value
    for i in range(shape[0]):
        # walk the second axis
        for j in range(shape[1]):
            # deposit a recognizable pattern
            srcview[i, j] = float(10 * i + j)

    # push the whole tile to disk
    dataset.write(data=src, memtype=memtype.htype, origin=[0, 0], shape=shape)

    # build a fresh buffer to receive the data
    dst = memtype.grid(shape=shape)
    # pull the tile back from disk
    dataset.read(data=dst, memtype=memtype.htype, origin=[0, 0], shape=shape)
    # view the recovered cells
    dstview = memoryview(dst)
    # every cell has to survive the round-trip
    for i in range(shape[0]):
        # over the second axis too
        for j in range(shape[1]):
            # what went out must come back
            assert dstview[i, j] == float(10 * i + j)

    # release the views before the buffers
    del srcview, dstview

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
