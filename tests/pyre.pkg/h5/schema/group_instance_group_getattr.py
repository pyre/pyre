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
    class Meta(pyre.h5.schema.group):
        """
        A group of datasets in some HDF5 file
        """

        # something boring
        flag = pyre.h5.schema.bool()
        flag.default = True
        flag.doc = "a boolean"

        # something simple
        answer = pyre.h5.schema.int()
        answer.default = 42
        answer.doc = "the answer to the ultimate question"

        # a compatible container
        pols = pyre.h5.schema.strings()
        pols.default = "HH", "HV", "VH", "VV"
        pols.doc = "the list of polarizations"

    # embed it in another group
    class Group(pyre.h5.schema.group):
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
    assert meta.flag.default is True
    #  the int
    assert meta.answer.default == 42
    # the polarizations
    assert meta.pols.default == ["HH", "HV", "VH", "VV"]

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
