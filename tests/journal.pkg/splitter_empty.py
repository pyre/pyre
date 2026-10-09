#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test() -> None:
    """
    Verify that a splitter skips its empty attachments and forwards to the rest
    """
    # access
    import journal

    # the entries that reach the device
    seen = []

    # a device that records the sinks it is handed entries through
    class Capture(journal.device):
        """
        A device that records the sinks it is handed entries through
        """

        def alert(self, entry: journal.entry) -> "Capture":
            """
            Record a user facing {entry}
            """
            # note the sink
            seen.append("alert")
            # all done
            return self

        def help(self, entry: journal.entry) -> "Capture":
            """
            Record a help {entry}
            """
            # note the sink
            seen.append("help")
            # all done
            return self

        def memo(self, entry: journal.entry) -> "Capture":
            """
            Record a developer facing {entry}
            """
            # note the sink
            seen.append("memo")
            # all done
            return self

    # make a splitter with an empty attachment ahead of the device
    splitter = journal.splitter(outputs=[None, Capture(name="capture")])
    # make an entry
    entry = journal.entry(page=[], notes={})
    # send it through each sink
    splitter.alert(entry=entry).help(entry=entry).memo(entry=entry)
    # the device got all three
    assert seen == ["alert", "help", "memo"]

    # all done
    return


# main
if __name__ == "__main__":
    # skip the bindings, so the pure python implementation is exercised
    journal_no_libjournal = True
    # run the test
    test()


# end of file
