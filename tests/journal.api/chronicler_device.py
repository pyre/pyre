#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that we can set the global default device
    """
    # access
    import journal

    # get the global state
    chronicler = journal.chronicler

    # verify that the default device is the console
    assert chronicler.device.name == "cout"

    # make a trash can
    trash = journal.trash()
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
