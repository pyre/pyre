#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Exercise handing a transfer property list to a read and to a write

    The transfer list is the only place a caller can say what should happen to cells while
    they are in flight: the size of the conversion buffer, whether checksums are verified,
    and the data transform, which is an arithmetic expression the library applies to every
    value as it crosses. Until now one could be built and never used, because every read and
    write named the library default instead.

    The transform is what makes this visible from a test: with it, the same cells come back
    different, and the difference is exactly the expression. It also pins the direction --
    a transform on the way out and a transform on the way in are separate events, and
    applying one on each is how a round trip can end up back where it started
    """
    # get the bindings
    from pyre.extensions import libh5

    # for a scratch path and a payload
    import os
    import array

    # a scratch data product
    uri = "transfer_list.h5"
    # make sure a stale one is not lying around
    if os.path.exists(uri):
        # by removing it
        os.remove(uri)

    # the layout: a handful of cells is plenty to see a transform take effect
    extent = [4, 4]
    # and the number of cells
    cells = extent[0] * extent[1]

    # make the file
    f = libh5.File(uri=uri, mode="w")
    # describe the extent
    space = libh5.DataSpace(shape=extent)
    # a dataset to read back from
    src = f.create(path="src", type=libh5.types.native.double, space=space)
    # and one to write through a transform into
    dst = f.create(path="dst", type=libh5.types.native.double, space=space)

    # cells that count up, so a transform on them is easy to check by eye
    payload = array.array("d", (float(cell) for cell in range(cells)))
    # lay them down untouched
    src.write(payload, libh5.types.native.double, [0, 0], extent)

    # read them back with nothing asked for: the default transfer list leaves them alone
    plain = array.array("d", bytes(cells * 8))
    # read
    src.read(plain, libh5.types.native.double, [0, 0], extent)
    # and check the first cell
    assert plain[0] == 0.0
    # and the last
    assert plain[cells - 1] == float(cells - 1)

    # now read the same cells through a transfer list that triples them on the way across
    tripling = libh5.properties.dxpl(expression="3*x")
    # make room for them
    tripled = array.array("d", bytes(cells * 8))
    # and read
    src.read(tripled, libh5.types.native.double, [0, 0], extent, [], tripling)
    # every value arrives multiplied
    for cell in range(cells):
        # by three
        assert tripled[cell] == 3.0 * payload[cell]

    # the dataset itself did not change: a transform lives in the transfer, not in the file;
    # make room
    again = array.array("d", bytes(cells * 8))
    # read plainly
    src.read(again, libh5.types.native.double, [0, 0], extent)
    # and check that the last cell holds what was written
    assert again[cells - 1] == float(cells - 1)

    # the write side takes one too: send the tripled values out through a transform that
    # divides by three, which should put the original values in the file
    thirding = libh5.properties.dxpl(expression="x/3")
    # write through it
    dst.write(tripled, libh5.types.native.double, [0, 0], extent, [], thirding)
    # read what landed, plainly, and it has to be what we started with; make room
    landed = array.array("d", bytes(cells * 8))
    # read
    dst.read(landed, libh5.types.native.double, [0, 0], extent)
    # go through the cells
    for cell in range(cells):
        # and compare each with the original
        assert landed[cell] == payload[cell]

    # and a transfer list composes with a stride: the two are independent settings, and the
    # transform has to apply to the samples the stride picked rather than to all of them
    stride = [2, 2]
    # the number of samples along each axis
    shape = [2, 2]
    # room for them
    sampled = array.array("d", bytes(shape[0] * shape[1] * 8))
    # read through both
    src.read(sampled, libh5.types.native.double, [0, 0], shape, stride, tripling)
    # walk the samples the stride would have chosen
    for row in range(shape[0]):
        # row by row
        for col in range(shape[1]):
            # the cell each was drawn from
            sourceCell = (row * stride[0]) * extent[1] + col * stride[1]
            # tripled on its way here
            assert sampled[row * shape[1] + col] == 3.0 * payload[sourceCell]

    # clean up
    f.close()

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
