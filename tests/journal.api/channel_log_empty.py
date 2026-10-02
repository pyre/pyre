#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Verify that logging an empty message adds no line to the entry
    """
    # access
    import journal

    # a device that remembers the pages it receives
    class Capture(journal.device):
        """
        Record the page of every entry
        """

        def __init__(self, **kwds):
            """
            Start with nothing recorded
            """
            # chain up
            super().__init__(name="capture", **kwds)
            # nothing recorded yet
            self.pages = []
            # all done
            return

        def alert(self, entry):
            """
            Record the page of a user facing {entry}
            """
            # save a copy of the page
            self.pages.append(list(entry.page))
            # all done
            return self

        def memo(self, entry):
            """
            Record the page of a developer facing {entry}
            """
            # save a copy of the page
            self.pages.append(list(entry.page))
            # all done
            return self

    # make one
    capture = Capture()
    # make a channel
    channel = journal.info("tests.journal.empty")
    # that sends its entries to it
    channel.device = capture
    # flush with an empty message
    channel.log("")
    # no entry that reached the device has any lines
    assert all(page == [] for page in capture.pages), capture.pages

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
