#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Verify that the notes of a channel outlive the entry they were set on
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
    # the note is still there
    assert channel.notes["time"] == "then"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
