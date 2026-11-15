#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that dismissing a crew member never waits for it: the recruiter returns at once, a
member that does not leave within the grace period is told to go, one that ignores that is
removed, and the team hears of each departure on its event loop
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


def gone(pid):
    """
    Check whether the process {pid} is gone
    """
    # carefully
    try:
        # probe it
        os.kill(pid, 0)
    # if there is no such process
    except ProcessLookupError:
        # it is gone
        return True
    # otherwise, it is still around
    return False


# a stand-in for the team, with the event loop and the hook the recruiter needs
class Team:
    """
    A team that records when each of its members departed, and stops its event loop once all
    of them have
    """

    # interface
    def departed(self, crew, status):
        """
        The process of the {crew} member is gone
        """
        # record when
        self.departures[crew.pid] = time.monotonic() - self.start
        # once everybody has left
        if len(self.departures) == self.expected:
            # stop the event loop
            self.dispatcher.stop()
        # all done
        return self

    # metamethods
    def __init__(self, expected, **kwds):
        # chain up
        super().__init__(**kwds)
        # the name a team has, which the recruiter uses when it talks about my members
        self.pyre_name = "test.fork.dismiss.team"
        # the event loop
        self.dispatcher = pyre.ipc.newPSL()
        # how many members are expected to leave
        self.expected = expected
        # when each one did, by pid
        self.departures = {}
        # the start of the clock
        self.start = time.monotonic()
        # all done
        return


def test():
    # make a recruiter with a short grace period, so the test does not drag
    recruiter = pyre.nexus.fork()(name="test.fork.dismiss")
    recruiter.grace = 0.25 * second
    # and a team that expects three members to leave
    team = Team(expected=3)

    # a child that leaves when it is told to
    polite = stubborn(ignore=False)
    # a child that ignores polite requests
    deaf = stubborn(ignore=True)
    # and a child that has already left
    early = os.fork()
    # which, on its side of the fork
    if early == 0:
        # leaves at once
        os._exit(0)
    # give it time to do so
    time.sleep(0.1)

    # dismiss all three, and time it, from the moment of the dismissal
    start = team.start = time.monotonic()
    # go through the children
    for pid in (polite, deaf, early):
        # each one by its pid, which is all the recruiter needs to know about a member
        recruiter.dismiss(team=team, crew=types.SimpleNamespace(pid=pid))
    # how long that took
    elapsed = time.monotonic() - start
    # nobody waited for anybody
    assert elapsed < 0.1, elapsed
    # the child that had already left was collected on the spot
    assert early in team.departures, team.departures

    # in case something goes wrong, give up after a while
    team.dispatcher.alarm(interval=5 * second, call=lambda timestamp: team.dispatcher.stop())
    # let the event loop see the others leave
    team.dispatcher.watch()

    # the polite child left at the first reminder, after one grace period
    assert 0.25 <= team.departures[polite] < 0.5 + 0.25, team.departures
    # the deaf one at the second, after two
    assert 0.5 <= team.departures[deaf] < 0.75 + 0.25, team.departures
    # and every child is gone and harvested
    assert all(gone(pid) for pid in (polite, deaf, early))

    # all done
    return recruiter


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
