#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Sanity check: verify that the channel is accessible
    """
    # get the journal
    import journal

    # make a channel
    channel = journal.info(name="tests.journal.info")
    # verify the channel name
    assert channel.name == "tests.journal.info"
    # the detail should be at the default level
    assert channel.detail == 1
    # the channel should be active
    assert channel.active == True
    # and non fatal
    assert channel.fatal == False

    # the page should be empty
    assert list(channel.page) == []
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
