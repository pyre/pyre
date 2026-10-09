#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import gc


def test():
    """
    Verify that a device implemented in python keeps working as the device of a channel after python
    lets go of it
    """
    # access
    from journal import libjournal

    # the entries that reach the device
    seen = []

    # a device that records the pages of the entries it receives
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

    # make a channel
    channel = libjournal.Informational("tests.journal.device.python.channel")
    # install a device without holding on to it
    channel.device = Capture()
    # give python every chance to collect it
    gc.collect()

    # verify the channel still hands back the python device
    assert type(channel.device) is Capture

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
