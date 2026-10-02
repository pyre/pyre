#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Verify that an entry records where it was made without reading any source files
    """
    # externals
    import sys

    # get the journal
    import journal

    # a device that keeps the notes of the entries it receives
    class Capture(journal.device):
        # start with an empty log
        def __init__(self, **kwds):
            # chain up
            super().__init__(name="capture", **kwds)
            # nothing recorded yet
            self.notes = []

        # keep the notes of each entry, whatever its kind
        def alert(self, entry):
            # a user-facing alert
            self.notes.append(dict(entry.notes))
            # all done
            return self

        def memo(self, entry):
            # a developer-facing memo
            self.notes.append(dict(entry.notes))
            # all done
            return self

        def help(self, entry):
            # a help screen
            self.notes.append(dict(entry.notes))
            # all done
            return self

    # make the device
    capture = Capture()
    # and send all output to it
    journal.chronicler.device = capture
    # make a channel
    channel = journal.info(name="tests.journal.location")

    # the files the test opens
    opened = []

    # record the files that get opened
    def hook(event, args):
        """
        Watch for file opens
        """
        # if a file is being opened
        if event == "open":
            # record it
            opened.append(args[0])
        # all done
        return

    # watch
    sys.addaudithook(hook)
    # the line of the entry below
    line = sys._getframe().f_lineno + 2
    # make an entry
    channel.log("hello world!")

    # get the notes of the entry
    notes = capture.notes[0]
    # check that it recorded where it was made
    assert notes["filename"] == __file__
    assert notes["line"] == str(line)
    assert notes["function"] == "test"
    # and that nothing was read to find out
    assert not opened, opened

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
