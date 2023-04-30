#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


"""
Check that we can declare groups
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

    # sort its inheritance
    pedigree = Group.mro()
    # check it
    assert pedigree == [
        Group,
        pyre.h5.schema.group,
        pyre.h5.schema.descriptor,
        object,
    ]

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
