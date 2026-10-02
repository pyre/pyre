#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Verify that the lines of a report are indented just like the lines added one at a time
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
    channel = journal.info("tests.journal.report")
    # that sends its entries to it
    channel.device = capture
    # indent
    channel.indent()
    # add a line from a report
    channel.report(["text"])
    # and the same line by itself
    channel.line("text")
    # flush
    channel.log()
    # get the page of the entry
    (page,) = capture.pages
    # both lines were rendered the same way
    assert page[0] == page[1], page

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
