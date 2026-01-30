#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Verify the channel initial state
    """
    # access
    from journal.ext.journal import Debug as debug

    # make a channel
    channel = debug(name="tests.journal.debug")
    # verify the channel name
    assert channel.name == "tests.journal.debug"
    # the detail should be at the default level
    assert channel.detail == 1
    # the dent should be at the default level
    assert channel.dent == 0
    # the channel should be inactive
    assert channel.active is False
    # and non-fatal
    assert channel.fatal is False

    # the page should be empty
    assert tuple(channel.page) == ()
    # verify the metadata
    assert channel.notes["application"] == "journal"
    assert channel.notes["channel"] == channel.name
    assert channel.notes["severity"] == channel.severity

    # make a channel with name and detail
    channel = debug(name="tests.journal.debug", detail=2)
    # verify the channel name
    assert channel.name == "tests.journal.debug"
    # the detail should be 2
    assert channel.detail == 2
    # the dent should be at the default level
    assert channel.dent == 0
    # the channel should be inactive
    assert channel.active is False
    # and non-fatal
    assert channel.fatal is False

    # make a channel with name and dent
    channel = debug(name="tests.journal.debug", dent=1)
    # verify the channel name
    assert channel.name == "tests.journal.debug"
    # the detail should be 1
    assert channel.detail == 1
    # the dent should be 1
    assert channel.dent == 1
    # the channel should be inactive
    assert channel.active is False
    # and non-fatal
    assert channel.fatal is False

    # make a channel with name, detail, and dent
    channel = debug(name="tests.journal.debug", detail=2, dent=1)
    # verify the channel name
    assert channel.name == "tests.journal.debug"
    # the detail should be 2
    assert channel.detail == 2
    # the dent should be 1
    assert channel.dent == 1
    # the channel should be inactive
    assert channel.active is False
    # and non-fatal
    assert channel.fatal is False

    # verify setter for detail
    channel.detail = 3
    assert channel.detail == 3
    # verify setter for dent
    channel.dent = 3
    assert channel.dent == 3

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
