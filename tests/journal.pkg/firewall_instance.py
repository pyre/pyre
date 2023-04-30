#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify the channel initial state
    """
    # get the channel
    from journal.Firewall import Firewall as firewall

    # make a channel
    channel = firewall(name="tests.journal.firewall")
    # verify the channel name
    assert channel.name == "tests.journal.firewall"
    # the detail should be at the default level
    assert channel.detail == 1
    # it should be active
    assert channel.active == True
    # and fatal
    assert channel.fatal == True

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
