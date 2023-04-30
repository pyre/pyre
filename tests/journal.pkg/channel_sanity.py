#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# channel state interface
def test():
    """
    Exercise the channel state interface
    """
    # get the package
    from journal.Channel import Channel

    # derive a severity
    class Severity(Channel, active=False):
        """
        A sample derivation
        """

    # make one
    channel = Severity(name="test.channel")

    # verify its name
    assert channel.name == "test.channel"
    # its state
    assert channel.active == False
    # and again using the conversion to bool
    assert not channel
    # verify it is non-fatal
    assert channel.fatal == False

    # activate it
    channel.activate()
    # and check
    assert channel.active == True

    # make it fatal
    channel.fatal = True
    # and check
    assert channel.fatal == True

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
