#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# verify that we can control the default device
def test():
    """
    Verify that we can control the default device
    """
    # the trash can
    from journal.Trash import Trash as trash
    # get the channel
    from journal.Channel import Channel as channel

    # ask it for the default device
    builtin = channel.getDefaultDevice()

    # make new device
    custom = trash()
    # install it
    old = channel.setDefaultDevice(device=custom)

    # check that the default device is what we just installed
    assert channel.getDefaultDevice() is custom
    # and the device we just replaced was the original built-in one
    assert old is builtin

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
