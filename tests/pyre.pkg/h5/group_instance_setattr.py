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
    class Group(pyre.h5.group):
        """
        A group of datasets in some HDF5 file
        """

        # something boring
        flag = pyre.h5.bool()
        flag.default = "on"
        flag.pyre_doc = "have you got a flag?"

        # something simple
        id = pyre.h5.int()
        id.default = "42"
        id.pyre_doc = "a simple dataset"

        # something a bit more complicated
        pols = pyre.h5.list(schema=pyre.h5.str())
        pols.default = ("HH",)
        pols.pyre_doc = "a dataset that's a container"

    # instantiate
    group = Group()

    # verify the default state of the object
    assert group.flag.value is True
    assert group.id.value == 42
    assert group.pols.value == ["HH"]

    # make some assignments that will require conversions
    group.flag.value = "off"
    group.id.value = "1"
    group.pols.value = "HH", "HV", "VH", "VV"

    # verify the new state of the object
    assert group.flag.value is False
    assert group.id.value == 1
    assert group.pols.value == ["HH", "HV", "VH", "VV"]

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
