#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that we have write access to the global metadata and that channels inherit them automatically
    """
    # access
    import journal

    # get the global state
    chronicler = journal.chronicler

    # ask for the global metadata
    gNotes = chronicler.notes
    # adjust the application name
    gNotes["application"] = "chronicler"
    # and add something new
    gNotes["author"] = "michael"

    # now, make a channel
    channel = journal.debug(name="tests.journal.chronicler")
    # ask for its metadata
    cNotes = channel.notes
    # which must include the global settings above
    assert cNotes["application"] == "chronicler"
    assert cNotes["author"] == "michael"
    assert cNotes["channel"] == "tests.journal.chronicler"
    assert cNotes["severity"] == "debug"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
