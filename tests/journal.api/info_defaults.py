#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that the channel wide defaults are as expected
    """
    # access
    import journal

    # verify that info channels are active by default
    assert journal.info.defaultActive == True
    # and non-fatal
    assert journal.info.defaultFatal == False
    # verify that the channel default device is not set
    assert journal.info.defaultDevice == None

    # make a trash can
    trash = journal.trash()
    # make it the default device
    journal.info.defaultDevice = trash
    # and make sure the assignment sticks
    assert journal.info.defaultDevice is trash

    # make a channel
    channel = journal.info("test.channel")
    # verify that its view of its default state is consistent
    assert channel.defaultActive == journal.info.defaultActive
    assert channel.defaultFatal == journal.info.defaultFatal
    # similarly for the default device
    assert channel.defaultDevice == journal.info.defaultDevice

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
