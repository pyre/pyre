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
        flag = True

        # something simple
        answer = pyre.h5.int()
        answer.default = 42
        answer.doc = "the answer to the ultimate question"

    # instantiate
    group = Group()

    # verify we can read regular class attributes
    assert group.flag is True
    # check the answer
    assert group.answer == 42

    # all done
    return


# main
if __name__ == "__main__":
    # drive
    test()


# end of file
