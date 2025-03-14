#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


def test():
    """
    Verify that the firewall channel wide defaults are as expected
    """
    # access
    from journal import libjournal

    # verify that firewall channels are inactive by default
    assert libjournal.Firewall.defaultActive is True
    # and non-fatal
    assert libjournal.Firewall.defaultFatal is True
    # verify that the channel default device is not set
    assert libjournal.Firewall.defaultDevice == None

    # make a trash can
    trash = libjournal.Trash()
    # make it the default device
    libjournal.Firewall.defaultDevice = trash
    # and make sure the assignment sticks
    assert libjournal.Firewall.defaultDevice is trash

    # make a firewall channel
    channel = libjournal.Firewall("test.channel")
    # verify that its view of its default state is consistent
    assert channel.defaultActive == libjournal.Firewall.defaultActive
    assert channel.defaultFatal == libjournal.Firewall.defaultFatal
    # similarly for the default device
    assert channel.defaultDevice == libjournal.Firewall.defaultDevice

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
