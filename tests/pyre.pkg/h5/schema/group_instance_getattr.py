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
        flag = True

        # something simple
        answer = pyre.h5.schema.int()
        answer.default = 42
        answer.__doc__ = "the answer to the ultimate question"

        # a compatible container
        pols = pyre.h5.schema.strings()
        pols.default = ["HH", "HV", "VH", "VV"]
        pols.__doc__ = "the list of polarizations"

    # instantiate
    group = Group(name="root")

    # verify we can read regular class attributes
    assert group.flag is True

    # check the descriptor types
    assert isinstance(group.answer, pyre.h5.schema.int)
    assert isinstance(group.pols, pyre.h5.schema.list)

    # and their default values
    assert group.answer.default == 42
    assert group.pols.default == ["HH", "HV", "VH", "VV"]

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
