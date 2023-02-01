#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


"""
Check that we can harvest datasets from groups
"""


# the driver
def test():
    # support
    import pyre

    # make a group
    class Group(pyre.h5.schema.group):
        """
        A group of datasets in some HDF5 file
        """

        # something simple
        id = pyre.h5.schema.int()
        id.doc = "a simple dataset"

        # something a bit more complicated
        pols = pyre.h5.schema.list()
        pols.doc = "a dataset that's a container"

    # instantiate
    group = Group(name="root")

    # build the full set of my identifiers
    identifiers = {**Group._pyre_descriptors, **group._pyre_descriptors}
    # make sure it's the correct size
    assert len(identifiers) == 2
    # and check the contents
    assert identifiers["id"].typename == "int"
    assert identifiers["pols"].typename == "list"

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
