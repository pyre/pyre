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

    # declare a group layout
    class Group(pyre.h5.schema.group):
        """
        A group of datasets in some HDF5 file
        """

        # something simple
        id = pyre.h5.schema.int()
        id.doc = "a simple dataset"

        # something a bit more complicated
        pols = pyre.h5.schema.strings()
        pols.default = "HH", "VV"
        pols.doc = "a dataset that's a container"

    # now, make a group with this layout
    g = pyre.h5.api.group(at="/", layout=Group())

    # it has no subgroups
    assert tuple(g._pyre_groups()) == ()
    # and it has two datasets
    assert tuple(g._pyre_datasets()) == ("id", "pols")
    # for a total of two locations
    assert tuple(g._pyre_locations()) == ("id", "pols")

    # access the members
    assert g.id == 0
    assert g.pols == ["HH", "VV"]

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
