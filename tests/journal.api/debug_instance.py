#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


def test():
    """
    Verify the channel initial state
    """
    # access
    import journal

    # make a channel
    channel = journal.debug(name="tests.journal.debug")
    # verify the channel name
    assert channel.name == "tests.journal.debug"
    # the detail should be at the default level
    assert channel.detail == 1
    # the channel should be inactive
    assert channel.active == False
    # and non fatal
    assert channel.fatal == False

    # the page should be empty
    assert tuple(channel.page) == ()
    # verify the metadata
    assert channel.notes["application"] == "journal"
    assert channel.notes["channel"] == channel.name
    assert channel.notes["severity"] == channel.severity

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
