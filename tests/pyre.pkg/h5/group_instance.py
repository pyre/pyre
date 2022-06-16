#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2022 all rights reserved


"""
Check that we can harvest datasets from groups
"""


# the driver
def test():
    # support
    import pyre

    # make a group
    class Group(pyre.h5.group):
        """
        A group of datasets in some HDF5 file
        """
        # something simple
        id = pyre.h5.int()
        id.doc = "a simple dataset"

        # something a bit more complicated
        pols = pyre.h5.list()
        pols.doc = "a dataset that's a container"

    # instantiate
    group = Group()

    # verify that my table of identifiers is accessible
    identifiers = group.pyre_identifiers
    # and of the correct size
    assert len(identifiers) == 2
    # check the contents
    assert identifiers["id"].typename == "int"
    assert identifiers["pols"].typename == "list"

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file