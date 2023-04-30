#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# access to instance specific devices
def test():
    """
    Verify that channel instances get their devices from the same source, and that there is no
    crosstalk when setting a channel specific device
    """
    # get the support characters
    from journal.Trash import Trash
    # and the channel
    from journal.Channel import Channel

    # derive a severity
    class Severity(Channel, active=False):
        """
        A sample derivation
        """

    # make a trash can
    trash = Trash()

    # ask the chronicler for its device
    default = Severity.chronicler.device

    # make a couple of channels
    channel_1 = Severity("journal.tests.channel_1")
    channel_2 = Severity("journal.tests.channel_2")

    # verify that their device is currently what chronicler provides
    assert channel_1.device is default
    assert channel_2.device is default

    # set the channel wide default
    Severity.setDefaultDevice(trash)
    # and ask for it back
    shared = Severity.getDefaultDevice()
    # verify that that's what the two channels see now
    assert channel_1.device is shared
    assert channel_2.device is shared

    # set the channel specific devices to different values
    channel_1.device = Trash()
    channel_2.device = Trash()
    # verify the devices are now different
    assert channel_1.device is not channel_2.device

    # make a new channel that shares state with {channel_1}
    channel_10 = Severity("journal.tests.channel_1")
    # verify it has the same device
    assert channel_10.device is channel_1.device

    # make a new channel that shares state with {channel_2}
    channel_20 = Severity("journal.tests.channel_2")
    # verify it has the same device
    assert channel_20.device is channel_2.device

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
