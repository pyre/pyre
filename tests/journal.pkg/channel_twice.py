#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# channels with the same name share state
def test():
    """
    Verify that channels with the same name share state
    """
    # get the package
    from journal.Channel import Channel

    # derive a severity
    class Severity(Channel, active=False):
        """
        A sample derivation
        """

    # make one
    channel_1 = Severity(name="test.channel")
    # verify its name
    assert channel_1.name == "test.channel"
    # verify it is inactive
    assert channel_1.active == False
    # and again using the conversion to bool
    assert not channel_1
    # check that it is non-fatal
    assert channel_1.fatal == False

    # activate it
    channel_1.activate()
    # and check
    assert channel_1.active == True
    # make it fatal
    channel_1.fatal = True
    # and check
    assert channel_1.fatal == True

    # make another channel by the same name
    channel_2 = Severity(name="test.channel")
    # verify the name
    assert channel_2.name == "test.channel"
    # verify it's on
    assert channel_2.active == True
    # and fatal
    assert channel_2.fatal == True

    # deactivate it
    channel_2.active = False
    # verify
    assert channel_2.active == False
    # and that the new state is mirrored by channel_1
    assert channel_1.active == False

    # make it non-fatal
    channel_2.fatal = False
    # verify
    assert channel_2.fatal == False
    # and that the new state is mirrored by channel_1
    assert channel_1.fatal == False

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
