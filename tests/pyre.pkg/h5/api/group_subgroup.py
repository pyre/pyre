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

    # it has no members
    assert tuple(g._pyre_contents) == ()
    # no subgroups
    assert tuple(g._pyre_groups()) == ()
    # no datasets
    assert tuple(g._pyre_datasets()) == ()
    # and no locations
    assert tuple(g._pyre_locations()) == ()

    # all done
    return g


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
