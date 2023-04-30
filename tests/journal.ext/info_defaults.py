#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that the info channel wide defaults are as expected
    """
    # access
    from journal import libjournal

    # verify that info channels are inactive by default
    assert libjournal.Informational.defaultActive is True
    # and non-fatal
    assert libjournal.Informational.defaultFatal is False
    # verify that the channel default device is not set
    assert libjournal.Informational.defaultDevice == None

    # make a trash can
    trash = libjournal.Trash()
    # make it the default device
    libjournal.Informational.defaultDevice = trash
    # and make sure the assignment sticks
    assert libjournal.Informational.defaultDevice is trash

    # make a channel
    channel = libjournal.Informational("test.channel")
    # verify that its view of its default state is consistent
    assert channel.defaultActive == libjournal.Informational.defaultActive
    assert channel.defaultFatal == libjournal.Informational.defaultFatal
    # similarly for the default device
    assert channel.defaultDevice == libjournal.Informational.defaultDevice

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
