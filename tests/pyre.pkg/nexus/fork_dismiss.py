#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that dismissing a crew member cannot block forever: a member that does not leave within
the grace period is told to go, one that ignores that is removed, and either way the team gets
its process back
"""

# externals
import os
import signal
import time
import types

# support
import pyre
from pyre.units.SI import second


def stubborn(ignore):
    """
    Make a child process that will not leave on its own; with {ignore}, not even when asked
    """
    # clone
    pid = os.fork()
    # on the parent side
    if pid:
        # hand off the child
        return pid
    # on the child side: if asked to be deaf to polite requests
    if ignore:
        # ignore them
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
    # and sit here for far longer than any test is willing to wait
    time.sleep(600)
    # never reached, but just in case
    os._exit(0)


def test():
    # make a recruiter with a short grace period, so the test does not drag
    recruiter = pyre.nexus.fork()(name="test.fork.dismiss")
    recruiter.grace = 0.25 * second

    # a child that leaves when it is told to
    pid = stubborn(ignore=False)
    # dismiss it; all the recruiter needs to know about a member is its process id
    start = time.monotonic()
    recruiter.dismiss(team=None, crew=types.SimpleNamespace(pid=pid))
    elapsed = time.monotonic() - start
    # it took the grace period, and the polite request did the rest
    assert 0.25 <= elapsed < 0.5 + 0.25, elapsed
    # and the child is gone and harvested
    try:
        os.kill(pid, 0)
        assert False, "the child that was told to go is still around"
    except ProcessLookupError:
        pass

    # a child that ignores polite requests
    pid = stubborn(ignore=True)
    # dismiss it
    start = time.monotonic()
    recruiter.dismiss(team=None, crew=types.SimpleNamespace(pid=pid))
    elapsed = time.monotonic() - start
    # it took two grace periods, and then it was removed
    assert 0.5 <= elapsed < 0.75 + 0.25, elapsed
    # and the child is gone and harvested
    try:
        os.kill(pid, 0)
        assert False, "the child that ignored the request is still around"
    except ProcessLookupError:
        pass

    # a child that has already left costs nothing
    pid = os.fork()
    if pid == 0:
        os._exit(0)
    time.sleep(0.1)
    start = time.monotonic()
    recruiter.dismiss(team=None, crew=types.SimpleNamespace(pid=pid))
    assert time.monotonic() - start < 0.1

    # all done
    return recruiter


# main
if __name__ == "__main__":
    test()


# end of file
