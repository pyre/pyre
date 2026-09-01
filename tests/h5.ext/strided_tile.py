#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Exercise reading and writing a tile that visits only every n-th cell

    Decimating a raster by pulling all of it and throwing most of it away moves cells nobody
    wanted. A strided selection asks the library to skip them instead, so the cost of a zoomed
    out view falls with the zoom rather than staying flat.

    The stride is per axis, since the two axes are decimated independently, and {shape} counts
    the samples that come back rather than the extent they were drawn from: the region swept
    is {shape} times {stride}. This pins that reading, in both directions, and checks that the
    samples really are the ones a caller would have picked out by hand
    """
    # get the bindings
    from pyre.extensions import libh5

    # for a scratch path and a payload
    import os
    import array

    # and for muzzling the complaint the mismatched stride is meant to raise
    import journal

    # a scratch data product
    uri = "strided_tile.h5"
    # make sure a stale one is not lying around
    if os.path.exists(uri):
        os.remove(uri)

    # the layout: a small raster whose cells each say where they live, so a sample can be
    # checked against the coordinate it claims to have come from
    extent = [32, 32]
    cells = extent[0] * extent[1]

    # make the file
    f = libh5.File(uri=uri, mode="w")
    # describe the extent
    space = libh5.DataSpace(shape=extent)
    # a dataset to read back from, and one to scatter into
    src = f.create(path="src", type=libh5.types.native.double, space=space)
    dst = f.create(path="dst", type=libh5.types.native.double, space=space)

    # every cell carries its own row and column, encoded so that either one can be recovered
    payload = array.array(
        "d", (float(100 * row + col) for row in range(extent[0]) for col in range(extent[1]))
    )
    # lay the whole raster down the ordinary way
    src.write(payload, libh5.types.native.double, [0, 0], extent)

    # now pull a decimated view: every second row and every fourth column, which is the case
    # that catches an implementation that assumes one stride for the whole request
    stride = [2, 4]
    shape = [8, 4]
    # somewhere to put the samples; they arrive packed, so the destination is the sample grid
    sampled = array.array("d", bytes(shape[0] * shape[1] * 8))
    src.read(sampled, libh5.types.native.double, [1, 3], shape, stride)

    # each sample has to be the cell a caller would have reached for by hand
    for row in range(shape[0]):
        for col in range(shape[1]):
            # the cell this sample was drawn from, walking out from the origin by the stride
            sourceRow = 1 + row * stride[0]
            sourceCol = 3 + col * stride[1]
            # and the value that cell was given when the raster was laid down
            assert sampled[row * shape[1] + col] == float(100 * sourceRow + sourceCol)

    # asking for no stride at all still means every cell of a solid block, which is what
    # every existing caller expects to keep getting
    solid = array.array("d", bytes(cells * 8))
    src.read(solid, libh5.types.native.double, [0, 0], extent)
    assert solid[0] == payload[0]
    assert solid[cells - 1] == payload[cells - 1]

    # the write side scatters: put the samples back into the second dataset at the same
    # spacing they were drawn from
    dst.write(sampled, libh5.types.native.double, [1, 3], shape, stride)

    # and read them back one at a time, to confirm they landed where they were aimed rather
    # than in a packed block at the corner
    one = array.array("d", bytes(8))
    for row in range(shape[0]):
        for col in range(shape[1]):
            # the slot this sample should have landed in
            targetRow = 1 + row * stride[0]
            targetCol = 3 + col * stride[1]
            # read that single cell
            dst.read(one, libh5.types.native.double, [targetRow, targetCol], [1, 1])
            # and it has to carry the value that travelled with it
            assert one[0] == float(100 * targetRow + targetCol)

    # a stride that does not speak for every axis is refused rather than guessed at; muzzle
    # the complaint so the suite stays silent on success
    channel = journal.error("pyre.h5")
    channel.device = journal.trash()
    channel.fatal = False
    # a buffer that would be big enough, so nothing but the stride is wrong here
    scratch = array.array("d", bytes(shape[0] * shape[1] * 8))
    # the complaint may or may not be fatal, depending on how the build wires the journal
    # across the language boundary; either way the read must not have happened
    try:
        src.read(scratch, libh5.types.native.double, [0, 0], shape, [2])
    except journal.ApplicationError:
        pass
    # nothing was read, so the buffer is still as it started
    assert scratch[0] == 0.0

    # clean up
    f.close()

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
