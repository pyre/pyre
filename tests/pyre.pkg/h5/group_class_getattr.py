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
        flag = True

        # something simple
        answer = pyre.h5.int()
        answer.default = 42
        answer.pyre_doc = "the answer to the ultimate question"

    # verify we can read regular class attributes
    assert Group.flag is True

    # get the identifier
    answer = Group.answer
    # verify that accessing an identifier returns its descriptor
    assert isinstance(answer, pyre.h5.int)
    # and that we have access to its metadata
    assert answer.default == 42
    assert answer.pyre_doc == "the answer to the ultimate question"

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
