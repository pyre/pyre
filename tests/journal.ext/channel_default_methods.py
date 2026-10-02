#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    The severity wide device is also accessible through methods
    """
    # get the bindings
    from journal import libjournal

    # initially, there is no severity wide device
    assert libjournal.Informational.getDefaultDevice() is None
    # make a trash can
    trash = libjournal.Trash()
    # install it and get the previous setting
    old = libjournal.Informational.setDefaultDevice(device=trash)
    # which was empty
    assert old is None
    # verify the assignment sticks
    assert libjournal.Informational.getDefaultDevice() is trash
    # and it is visible as a property
    assert libjournal.Informational.defaultDevice is trash
    # restore the default and verify that the trash can comes back
    assert libjournal.Informational.setDefaultDevice(device=None) is trash

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
