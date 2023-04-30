#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that the device base class constructor is unavailable
    """
    # access
    from journal import libjournal

    # get the global state
    chronicler = libjournal.Chronicler

    # verify that the default device is the console
    assert chronicler.device.name == "cout"

    # make a trash can
    trash = libjournal.Trash()
    # set it as the device
    chronicler.device = trash
    # verify the assignment sticks
    assert chronicler.device is trash
    # and that the name is correct
    assert chronicler.device.name == "trash"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
