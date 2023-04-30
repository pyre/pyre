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

    # verify that error channels are inactive by default
    assert journal.error.defaultActive == True
    # and fatal
    assert journal.error.defaultFatal == True
    # verify that the channel default device is not set
    assert journal.error.defaultDevice == None

    # make a trash can
    trash = journal.trash()
    # make it the default device
    journal.error.defaultDevice = trash
    # and make sure the assignment sticks
    assert journal.error.defaultDevice is trash

    # make an error channel
    channel = journal.error("test.channel")
    # verify that its view of its default state is consistent
    assert channel.defaultActive == journal.error.defaultActive
    assert channel.defaultFatal == journal.error.defaultFatal
    # similarly for the default device
    assert channel.defaultDevice == journal.error.defaultDevice

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
