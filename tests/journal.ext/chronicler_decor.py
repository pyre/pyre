#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that we can control the minimum decor level
    """
    # access
    from journal import libjournal

    # get the global state
    chronicler = libjournal.Chronicler

    # verify that the decor level is at its default value
    assert chronicler.decor == 1
    # set it to some other value
    chronicler.decor = 5
    # verify the assignment sticks
    assert chronicler.decor == 5

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
