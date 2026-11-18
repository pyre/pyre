#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    A {BootDevice} buffers entries while pyre is booting and replays them, in order, on demand
    """
    # get the boot device
    from journal.BootDevice import BootDevice

    # a capturing stand-in for the real device a handoff would install
    class Capture:
        """
        A device that records which sink each entry reached
        """

        def __init__(self, **kwds):
            """
            Start with an empty log
            """
            # chain up
            super().__init__(**kwds)
            # nothing recorded yet
            self.calls = []
            # all done
            return

        def alert(self, entry):
            """
            Record a user-facing alert
            """
            # add it to the log
            self.calls.append(("alert", entry))
            # all done
            return

        def memo(self, entry):
            """
            Record a developer-facing memo
            """
            # add it to the log
            self.calls.append(("memo", entry))
            # all done
            return

        def help(self, entry):
            """
            Record a help screen
            """
            # add it to the log
            self.calls.append(("help", entry))
            # all done
            return

    # a fresh boot device
    boot = BootDevice()
    # entries across all three sinks are buffered, not rendered, and keep their arrival order:
    # a memo
    boot.memo(entry="m1")
    # an alert
    boot.alert(entry="a1")
    # and a help screen
    boot.help(entry="h1")
    # nothing has been sent anywhere yet, only stashed
    assert boot.buffer == [("memo", "m1"), ("alert", "a1"), ("help", "h1")]

    # replaying sends each entry to its matching sink on the target device, in order; make one
    capture = Capture()
    # replay the buffer onto it
    boot.replay(capture)
    # and check what arrived, and in what order
    assert capture.calls == [("memo", "m1"), ("alert", "a1"), ("help", "h1")]
    # and the buffer is drained afterward
    assert boot.buffer == []

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
