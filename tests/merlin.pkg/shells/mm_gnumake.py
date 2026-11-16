#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The check of GNU make accepts a recent enough version silently, and complains about one that
is too old, a program that is not GNU make, one that fails, and one that is not there
"""


def test() -> None:
    """
    Point the check at stand-ins for make, one for each outcome, and look at what it says
    """
    # externals
    import os
    import tempfile

    # support
    import journal
    from merlin.shells.MM import MM

    # a device that remembers the entries it receives
    class Capture(journal.device):
        """
        Remember the pages of the entries that reach me
        """

        # meta-methods
        def __init__(self, **kwds):
            # chain up
            super().__init__(name="capture", **kwds)
            # nothing received yet
            self.pages = []
            # all done
            return

        # interface
        def alert(self, entry):
            """
            Remember an entry meant for users
            """
            # save its page
            self.pages.append(list(entry.page))
            # all done
            return self

        def memo(self, entry):
            """
            Remember an entry meant for developers
            """
            # save its page
            self.pages.append(list(entry.page))
            # all done
            return self

        def help(self, entry):
            """
            Remember a help screen
            """
            # save its page
            self.pages.append(list(entry.page))
            # all done
            return self

    # get the channel of the check
    channel = journal.error("mm.gnu")
    # make its complaints survivable, so each case reports and returns
    channel.fatal = False
    # and capture them
    capture = Capture()
    # by sending them to my device
    channel.device = capture

    # the stand-ins, what each one prints or does, and the first line of the complaint it gets
    cases = [
        ("recent", "echo 'GNU Make 4.4.1'", None),
        ("old", "echo 'GNU Make 3.81'", "your version of GNU make is too old"),
        ("other", "echo 'BSD make'", "could not find a suitable installation of GNU make"),
        ("failing", "exit 2", "failed to launch"),
        ("missing", None, "an unexpected error occurred"),
    ]

    # build the application
    app = MM(name="mm-gnumake")
    # in a scratch directory that goes away when we are done
    with tempfile.TemporaryDirectory() as scratch:
        # go through the cases
        for name, script, complaint in cases:
            # the path to the stand-in
            make = os.path.join(scratch, name)
            # if it is supposed to exist
            if script is not None:
                # write it
                with open(make, "w") as stream:
                    # as a shell script
                    stream.write(f"#!/bin/sh\n{script}\n")
                # and make it executable
                os.chmod(make, 0o755)
            # point the check at it
            app.make = make
            # forget what earlier cases said
            capture.pages.clear()
            # run the check
            result = app.verifyGNUMake()
            # it must return, rather than raise
            assert result is None, f"{name}: {result!r}"
            # a recent version
            if complaint is None:
                # gets no complaint
                assert not capture.pages, f"{name}: {capture.pages}"
                # and that's all
                continue
            # the others get exactly one
            assert len(capture.pages) == 1, f"{name}: {capture.pages}"
            # that starts as expected
            assert capture.pages[0][0].startswith(complaint), f"{name}: {capture.pages[0]}"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
