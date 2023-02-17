#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


"""
Check that we can decorate groups with schema
"""


def test():
    # support
    import pyre

    # declare the metadata group layout
    class Meta(pyre.h5.schema.group):
        """
        A group of datasets in some HDF5 file
        """

        # something simple
        id = pyre.h5.schema.int()
        id.__doc__ = "a simple dataset"

        # something a bit more complicated
        pols = pyre.h5.schema.strings()
        pols.default = "HH", "VV"
        pols.__doc__ = "a dataset that's a container"

    # and the main group layout
    class Group(pyre.h5.schema.group):
        """
        The top level group
        """

        # add the metadata
        meta = Meta()

    # now, make a group with this layout
    g = pyre.h5.api.group(at="/", layout=Group())

    # make a subgroup
    extra = pyre.h5.schema.group(name="extra")
    # add a dataset to it
    flag = pyre.h5.schema.bool(default=False)
    # attach it to the subgroup
    extra.flag = flag
    # and add the whole thing as a subgroup of {meta}
    g.meta.extra = extra

    # check the assignment happened successfully
    assert g.meta.extra.flag == False
    # modify
    g.meta.extra.flag = "on"
    # and check that the modification took place and the data coercion was successful
    assert g.meta.extra.flag == True

    # all done
    return g


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
