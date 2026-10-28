#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that asking a tracker for the history of a key it never tracked leaves no record behind
"""


def test() -> None:
    """
    Ask for the history of an untracked key, then check the log
    """
    # get the package
    import pyre.tracking

    # make a tracker
    tracker = pyre.tracking.tracker()
    # track one key
    tracker.track(key="kerf", node=3.2)

    # a key that was never tracked has no history
    assert tracker.getHistory(key="depth") == []
    # and asking about it didn't add it to the log
    assert "depth" not in tracker.log
    # while the tracked key keeps its history
    assert tracker.getHistory(key="kerf") == [3.2]

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
