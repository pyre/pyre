#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that the error channel wide defaults are as expected
    """
    # access
    from journal import libjournal

    # verify that error channels are active by default
    assert libjournal.Error.defaultActive is True
    # and fatal
    assert libjournal.Error.defaultFatal is True
    # verify that the channel default device is not set
    assert libjournal.Error.defaultDevice == None

    # make a trash can
    trash = libjournal.Trash()
    # make it the default device
    libjournal.Error.defaultDevice = trash
    # and make sure the assignment sticks
    assert libjournal.Error.defaultDevice is trash

    # make a channel
    channel = libjournal.Error("test.channel")
    # verify that its view of its default state is consistent
    assert channel.defaultActive == libjournal.Error.defaultActive
    assert channel.defaultFatal == libjournal.Error.defaultFatal
    # similarly for the default device
    assert channel.defaultDevice == libjournal.Error.defaultDevice

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
