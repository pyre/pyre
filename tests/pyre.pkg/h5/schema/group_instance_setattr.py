#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


"""
Exercise assignments to class attributes
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

        # something boring
        flag = pyre.h5.schema.bool()
        flag.default = "on"
        flag.doc = "have you got a flag?"

        # something simple
        id = pyre.h5.schema.int()
        id.default = "42"
        id.doc = "a simple dataset"

        # something a bit more complicated
        pols = pyre.h5.schema.list(schema=pyre.h5.schema.str())
        pols.default = ("HH",)
        pols.doc = "a dataset that's a container"

    # instantiate
    group = Group()

    # verify the default state of the object
    assert group.flag.default == "on"
    assert group.id.default == "42"
    assert group.pols.default == ["HH"]

    # make some assignments that will require conversions
    group.flag = "off"
    group.id = "1"
    group.pols = "HH", "HV", "VH", "VV"

    # verify the new state of the object
    assert group.flag.default == "off"
    assert group.id.default == "1"
    assert group.pols.default == ("HH", "HV", "VH", "VV")

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
