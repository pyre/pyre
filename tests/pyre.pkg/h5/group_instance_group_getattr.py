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

    # make a group with some data
    class Meta(pyre.h5.group):
        """
        A group of datasets in some HDF5 file
        """

        # something boring
        flag = pyre.h5.bool()
        flag.default = True
        flag.pyre_doc = "a boolean"

        # something simple
        answer = pyre.h5.int()
        answer.default = 42
        answer.pyre_doc = "the answer to the ultimate question"

        # a compatible container
        pols = pyre.h5.list(schema=pyre.h5.str())
        pols.default = "HH", "HV", "VH", "VV"
        pols.pyre_doc = "the list of polarizations"

    # embed it in another group
    class Group(pyre.h5.group):
        """
        A group that contains a subgroup
        """

        # the subgroup
        meta = Meta()

    # instantiate
    group = Group()

    # get the subgroup
    meta = group.meta
    # verify that each time we ask for it we get the exact same object
    assert meta is group.meta

    # verify we can read through the subgroup
    # the flag
    assert meta.flag.value is True
    #  the int
    assert meta.answer.value == 42
    # check the polarizations
    pols = meta.pols.value
    # verify the tuple has been converted into a list
    assert type(pols) is list
    # verify the contents are all strings
    assert tuple(map(type, pols)) == (str, str, str, str)
    # check the actual values
    assert pols == ["HH", "HV", "VH", "VV"]

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
