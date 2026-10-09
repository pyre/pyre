#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import gc


def test() -> None:
    """
    Verify that a python device nested in splitters keeps working after python lets go of it,
    and that the process exits cleanly with it still installed
    """
    # access
    from journal import libjournal

    # the entries that reach the python device
    seen = []

    # a device implemented in python
    class Capture(libjournal.Device):
        """
        A device that records the pages of the entries it receives
        """

        def __init__(self, **kwds) -> None:
            """
            Build a device named after its purpose
            """
            # chain up
            super().__init__(name="capture", **kwds)
            # all done
            return

        def alert(self, entry: libjournal.Entry) -> "Capture":
            """
            Record the page of a user facing {entry}
            """
            # save the page
            seen.append(list(entry.page))
            # all done
            return self

        def help(self, entry: libjournal.Entry) -> "Capture":
            """
            Record the page of a help {entry}
            """
            # save the page
            seen.append(list(entry.page))
            # all done
            return self

        def memo(self, entry: libjournal.Entry) -> "Capture":
            """
            Record the page of a developer facing {entry}
            """
            # save the page
            seen.append(list(entry.page))
            # all done
            return self

    # make an inner splitter over a python device
    inner = libjournal.Splitter(outputs=[Capture()])
    # make an outer splitter over the inner one
    outer = libjournal.Splitter(outputs=[inner])
    # make the outer splitter the default device
    libjournal.Chronicler.device = outer
    # let go of the splitters
    del inner, outer
    # and give python every chance to collect the python device
    gc.collect()

    # make a channel
    channel = libjournal.Informational("tests.journal.device.python.nested")
    # say something
    channel.log("hello")
    # verify the entry made it to the python device
    assert seen == [["hello"]]

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
