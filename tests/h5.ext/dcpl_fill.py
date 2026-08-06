#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Exercise the dataset fill value: chunks that were never written read back as the declared
    fill, not as garbage
    """
    # get the bindings
    from pyre.extensions import libh5

    # for a scratch path and its cleanup
    import os

    # a scratch data product
    uri = "h5_ext_dcpl_fill.h5"
    # make sure a stale one is not lying around
    if os.path.exists(uri):
        os.remove(uri)

    # make the file
    f = libh5.File(uri=uri, mode="w")
    # describe the extent
    space = libh5.DataSpace(shape=[100, 100])
    # the creation properties: chunked, with a declared fill value
    dcpl = libh5.properties.dcpl()
    dcpl.chunk = [30, 40]
    dcpl.fillValue = -1.0
    # the property list records that the declaration is mine rather than the library's
    assert dcpl.fillValueStatus == libh5.FillValue.user_defined
    # make the dataset
    dataset = f.create(path="product", type=libh5.types.native.double, space=space, dcpl=dcpl)

    # a reader pulls a chunk that nothing ever wrote
    m = dataset.mosaic(cell="float64")
    # bring it in
    m.fill(tile=[1, 1])
    # every cell holds the declared fill value, not garbage
    assert m[35, 45] == -1.0
    assert m[59, 79] == -1.0

    # and the dataset answers for its own fill value, with no type to name and nothing to
    # get wrong: it reads the value in the terms it actually holds
    assert dataset.fillValue == -1.0

    # a dataset nobody gave one to still has a fill value, because hdf5 supplies zero; the
    # status is what separates that from a value someone chose
    plain = f.create(path="plain", type=libh5.types.native.double, space=space)
    assert plain.dcpl.fillValueStatus == libh5.FillValue.default
    assert plain.fillValue == 0.0

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
