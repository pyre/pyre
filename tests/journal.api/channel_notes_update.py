#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Verify that a note set again on a later entry of the same channel takes the new value
    """
    # access
    import journal

    # make a channel
    channel = journal.info("tests.journal.notes")
    # send its output to the trash
    channel.device = journal.trash()
    # set a note
    channel.notes["time"] = "then"
    # record an entry
    channel.log("first")
    # give the note a new value
    channel.notes["time"] = "now"
    # record another entry
    channel.log("second")
    # the note holds the latest value
    assert channel.notes["time"] == "now"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
