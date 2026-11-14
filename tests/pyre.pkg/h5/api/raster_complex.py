#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise datasets of complex numbers whose parts the file names its own way, {real} and {imag}.
The read path recognizes them as complex numbers, and every access strategy delivers a pixel with
its parts in place, lined up with the members of the file by position
"""


def test():
    # support
    import pyre
    import struct

    # without the bindings
    if pyre.libpyre is None:
        # there is nothing to test
        return
    # get the h5 bindings
    libh5 = pyre.h5.libh5
    # without them
    if libh5 is None:
        # there is nothing to test either
        return

    # the value at a pixel
    def value(row, col):
        """
        The complex number stored at {row}, {col}
        """
        # make one out of the position
        return complex(10 * row + col, -(10 * row + col))

    # the product
    uri = pyre.primitives.path("raster_complex.h5")

    # the producer: build the file through the bindings
    root = pyre.h5.api.file()._pyre_local(uri=uri, mode="w")._pyre_id
    # the stored layout: two floats named the way some producers name them
    stored = libh5.types.compound(8)
    # the real part first
    stored.insert("real", 0, libh5.types.native.float)
    # and the imaginary part after it
    stored.insert("imag", 4, libh5.types.native.float)
    # make a raster of them
    raster = root.create(path="values", type=stored, space=libh5.DataSpace(shape=[2, 3]))
    # pack the values, row by row
    payload = struct.pack(
        "=12f",
        *(
            part
            for row in range(2)
            for col in range(3)
            for part in (value(row, col).real, value(row, col).imag)
        ),
    )
    # write them
    raster.write(data=bytearray(payload), memtype=stored, origin=[0, 0], shape=[2, 3])
    # let go of the handles, closing the file
    del raster, root

    # the consumer: the pkg read path
    product = pyre.h5.read(uri=uri)
    # the raster of values
    values = product.values
    # knows its geometry
    assert values.shape == [2, 3]
    # and that its cells are single precision complex numbers
    assert values.memtype.cell == "complex64"

    # the dense strategy: a private tile on the heap
    tile = values.tile()
    # every pixel has its parts in place
    for row in range(2):
        # column by column
        for col in range(3):
            # check
            assert tile[row, col] == value(row, col)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
