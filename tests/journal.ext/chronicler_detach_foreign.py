#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import gc
import weakref


def test() -> None:
    """
    Verify that detaching the foreign devices releases the python devices and leaves a console
    as the default device
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

    # make a python device
    device = Capture()
    # watch it
    watch = weakref.ref(device)
    # install it as the default
    libjournal.Chronicler.device = device
    # and as the device of a channel
    libjournal.Informational("tests.journal.detach.foreign").device = device
    # let go of it
    del device

    # detach the foreign devices
    libjournal.Chronicler.detachForeign()
    # and give python every chance to collect it
    gc.collect()

    # the python device is gone
    assert watch() is None
    # the default device is a console
    assert type(libjournal.Chronicler.device) is libjournal.Console

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
