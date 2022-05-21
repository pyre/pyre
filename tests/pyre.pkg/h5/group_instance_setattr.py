#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2022 all rights reserved


"""
Exercise assignments to class attributes
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
        # something boring
        flag = pyre.h5.bool()
        flag.default = "on"
        flag.doc = "have you got a flag?"

        # something simple
        id = pyre.h5.int()
        id.default = "42"
        id.doc = "a simple dataset"

        # something a bit more complicated
        pols = pyre.h5.list(schema=pyre.h5.str())
        pols.default = "HH",
        pols.doc = "a dataset that's a container"

    # instantiate
    group = Group()

    # verify the default state of the object
    assert group.flag is True
    assert group.id == 42
    assert group.pols == ["HH"]

    # make some assignments that will require conversions
    group.flag = "off"
    group.id = "1"
    group.pols = "HH", "HV", "VH", "VV"

    # verify the new state of the object
    assert group.flag is False
    assert group.id == 1
    assert group.pols == ["HH", "HV", "VH", "VV"]

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
