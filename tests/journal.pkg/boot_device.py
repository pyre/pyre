#!/usr/bin/env python3
# -*- Python -*-
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
        # start with an empty log
        def __init__(self):
            # nothing recorded yet
            self.calls = []

        # record which sink each entry reached
        def alert(self, entry):
            # a user-facing alert
            self.calls.append(("alert", entry))

        def memo(self, entry):
            # a developer-facing memo
            self.calls.append(("memo", entry))

        def help(self, entry):
            # a help screen
            self.calls.append(("help", entry))

    # a fresh boot device
    boot = BootDevice()
    # entries across all three sinks are buffered, not rendered, and keep their arrival order
    boot.memo(entry="m1")
    boot.alert(entry="a1")
    boot.help(entry="h1")
    # nothing has been sent anywhere yet, only stashed
    assert boot.buffer == [("memo", "m1"), ("alert", "a1"), ("help", "h1")]

    # replaying sends each entry to its matching sink on the target device, in order
    capture = Capture()
    boot.replay(capture)
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
