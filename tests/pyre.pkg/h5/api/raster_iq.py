#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise datasets of radar samples: cells that are a compound of two integers, named the way the
files of the mission name them, {r} and {i}. The read path recognizes them as samples, hands the
dataset of them back as a raster whose cells are {iq}, and every access strategy delivers a pixel
as the pair of its counts, in order, whatever the members are called; a dataset that holds one
sample reads whole as the pair, and one that holds more refuses to.
"""


def test():
    # support
    import journal
    import pyre
    import struct

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

    # the sample at each position, each count with its own value
    def sample(row, col):
        # the in-phase count encodes the position, the quadrature one its mirror
        return (10 * row + col, 65535 - (10 * row + col))

    # place the test file
    uri = pyre.primitives.path("raster_iq.h5")

    # the producer: write the samples the way the mission writes them
    # create the file and grab the low level handle, which doubles as the root group
    root = pyre.h5.api.file()._pyre_local(uri=uri, mode="w")._pyre_id
    # the stored layout: two unsigned 16-bit counts named {r} and {i}
    stored = libh5.types.compound(4)
    # the first count, named {r}
    stored.insert("r", 0, libh5.types.native.uint16)
    # and the second, named {i}
    stored.insert("i", 2, libh5.types.native.uint16)
    # a raster of them
    raster = root.create(path="samples", type=stored, space=libh5.DataSpace(shape=[2, 3]))
    # the samples, laid out as the two counts back to back, row by row
    payload = struct.pack(
        "=12H", *(count for row in range(2) for col in range(3) for count in sample(row, col))
    )
    # write them
    raster.write(data=bytearray(payload), memtype=stored, origin=[0, 0], shape=[2, 3])
    # and a dataset that holds a single sample
    single = root.create(path="sample", type=stored, space=libh5.DataSpace(shape=[1]))
    # written the same way
    single.write(data=bytearray(struct.pack("=2H", 7, 8)), memtype=stored, origin=[0], shape=[1])
    # read whole, it comes back as the pair of its counts
    assert single.iq() == (7, 8)
    # a raster of samples is not one sample, so reading it as one is refused; the refusal is
    # expected, so its entry goes to the trash rather than the console
    journal.error("pyre.h5.dataset.iq").device = journal.trash()
    # attempt it
    try:
        # which is refused
        raster.iq()
    # the refusal is an error, and errors are fatal by default
    except journal.ApplicationError:
        # as expected
        pass
    # anything else
    else:
        # is a failure
        assert False, "a raster was read as a single sample"
    # let go of the handles, closing the file
    del raster, single, root

    # the consumer: the pkg read path
    product = pyre.h5.read(uri=uri)
    # the raster of samples
    value = product.samples
    # knows its geometry
    assert value.shape == [2, 3]
    # and that its cells are samples of unsigned 16-bit counts
    assert value.memtype.cell == "iquint16"

    # the dense strategy: a private tile on the heap
    tile = value.tile()
    # every pixel is the pair of its counts, in order
    for row in range(2):
        # column by column
        for col in range(3):
            # check
            assert tile[row, col] == sample(row, col)

    # the out-of-core strategy: a mosaic over the dataset
    mosaic = value.mosaic()
    # pull in the tile that holds a pixel
    mosaic.fill(tile=mosaic.tileOf(index=[1, 2]))
    # and the pixel is the pair of its counts
    assert mosaic[1, 2] == sample(1, 2)

    # a schema that declares the samples as complex numbers
    class Product(pyre.h5.schema.group):
        """
        A product that mistakes its radar samples for complex numbers
        """

        # the samples
        samples = pyre.h5.schema.array(schema=pyre.h5.schema.complex(), shape=[2, 3])

    # is refused: integers are never complex; the refusal is a warning, which is expected, so
    # its entry goes to the trash rather than the console
    journal.warning("pyre.h5.api.inspector").device = journal.trash()
    # read the product through the schema
    queried = pyre.h5.read(uri=uri, query=Product(name="root"))
    # and the samples come back as samples, not as complex numbers
    assert queried.samples.memtype.cell == "iquint16"
    # with every pixel the pair of its counts
    assert queried.samples.tile()[1, 2] == sample(1, 2)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
