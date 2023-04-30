#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that we can control the minimum detail level
    """
    # access
    from journal import libjournal

    # get the global state
    chronicler = libjournal.Chronicler

    # verify that the detail level is at its default value
    assert chronicler.detail == 1
    # set it to some other value
    chronicler.detail = 5
    # verify the assignment sticks
    assert chronicler.detail == 5

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
