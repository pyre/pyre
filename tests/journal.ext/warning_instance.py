#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Verify the initial channel state
    """
    # get the channel
    from journal.ext.journal import Warning as warning

    # make a channel
    channel = warning(name="tests.journal.warning")
    # verify the channel name
    assert channel.name == "tests.journal.warning"
    # the detail should be at the default level
    assert channel.detail == 1
    # the dent should be at the default level
    assert channel.dent == 0
    # it should be active
    assert channel.active is True
    # and non-fatal
    assert channel.fatal is False

    # the page should be empty
    assert list(channel.page) == []
    # verify the metadata
    assert channel.notes["application"] == "journal"
    assert channel.notes["channel"] == channel.name
    assert channel.notes["severity"] == channel.severity

    # make a channel with name and detail
    channel = warning(name="tests.journal.warning", detail=2)
    # verify the channel name
    assert channel.name == "tests.journal.warning"
    # the detail should be at the default level
    assert channel.detail == 2
    # the dent should be 0
    assert channel.dent == 0
    # it should be active
    assert channel.active is True
    # and non-fatal
    assert channel.fatal is False

    # make a channel with name and dent
    channel = warning(name="tests.journal.warning", dent=1)
    # verify the channel name
    assert channel.name == "tests.journal.warning"
    # the detail should be at the default level
    assert channel.detail == 1
    # the dent should be 1
    assert channel.dent == 1
    # the channel should be active
    assert channel.active is True
    # and not fatal
    assert channel.fatal is False

    # make a channel with name, detail, and dent
    channel = warning(name="tests.journal.warning", detail=2, dent=1)
    # verify the channel name
    assert channel.name == "tests.journal.warning"
    # the detail should be at 2
    assert channel.detail == 2
    # the dent should be 1
    assert channel.dent == 1
    # the channel should be active
    assert channel.active is True
    # and not fatal
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
