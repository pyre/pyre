#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify te channel state
    """
    # get the channel
    from journal.Warning import Warning as warning

    # make a channel
    channel = warning(name="tests.journal.warning")
    # verify the channel name
    assert channel.name == "tests.journal.warning"
    # the detail should be at the default level
    assert channel.detail == 1
    # the channel should be active
    assert channel.active is True
    # and non-fatal
    assert channel.fatal is False

    # the page should be empty
    assert channel.page == []
    # verify the metadata
    assert channel.notes["application"] == "journal"
    assert channel.notes["channel"] == channel.name
    assert channel.notes["severity"] == channel.severity

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
