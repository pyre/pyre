#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that the debug channel wide defaults are as expected
    """
    # access
    from journal import libjournal

    # verify that debug channels are inactive by default
    assert libjournal.Debug.defaultActive is False
    # and non-fatal
    assert libjournal.Debug.defaultFatal is False
    # verify that the channel default device is not set
    assert libjournal.Debug.defaultDevice == None

    # make a trash can
    trash = libjournal.Trash()
    # make it the default device
    libjournal.Debug.defaultDevice = trash
    # and make sure the assignment sticks
    assert libjournal.Debug.defaultDevice is trash

    # make a debug channel
    channel = libjournal.Debug("test.channel")
    # verify that its view of its default state is consistent
    assert channel.defaultActive == libjournal.Debug.defaultActive
    assert channel.defaultFatal == libjournal.Debug.defaultFatal
    # similarly for the default device
    assert channel.defaultDevice == libjournal.Debug.defaultDevice

    # and now, the instance state
    assert channel.active == channel.defaultActive
    assert channel.fatal == channel.defaultFatal
    assert channel.device == channel.defaultDevice

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
