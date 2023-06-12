#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


"""
Check that we can decorate groups with schema
"""


# the driver
def test():
    # support
    import pyre
    import journal

    # make a channel
    channel = journal.debug("pyre.h5.api.writer")

    # declare the metadata group layout
    class Meta(pyre.h5.schema.group):
        """
        A group of datasets in some HDF5 file
        """

        # something simple
        id = pyre.h5.schema.int()
        id.__doc__ = "a simple dataset"

        # a string
        type = pyre.h5.schema.str()
        type.default = "SAMPLE"
        type.__doc__ = "the data product type"

        # something a bit more complicated
        pile = pyre.h5.schema.strings()
        pile.default = "HH", "VV"
        pile.__doc__ = "a dataset that's a container"

    # and the main group layout
    class Root(pyre.h5.schema.group):
        """
        The top level group
        """

        # add the metadata
        meta = Meta()

    # instantiate the product spec
    spec = Root(name="root")
    # show me
    spec._pyre_view(channel=channel)
    # realize it
    data = pyre.h5.api.assembler().visit(descriptor=spec)
    # adjust it
    data.meta.id = 7
    data.meta.type = "SOME PRODUCT DATA TYPE"
    data.meta.pile = "HH", "HV", "VH", "VV"
    # show me
    data._pyre_view(channel=channel)

    # pick a filename
    uri = "writer.h5"
    # write the file
    pyre.h5.write(uri=uri, data=data)
    # read it back in
    recovered = pyre.h5.read(uri=uri)

    # check
    assert recovered.meta.id == data.meta.id
    assert recovered.meta.type == data.meta.type
    assert recovered.meta.pile == data.meta.pile

    # all done
    return data


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
