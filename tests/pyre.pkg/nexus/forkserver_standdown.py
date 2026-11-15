#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a staff recruited through the forkserver stands down promptly: standing down waits
for nobody, every member is told to leave at once, and the staffing agency reports each exit as
it happens, so the whole staff is gone in a fraction of the time it would take to see the
members out one at a time
"""

# externals
import os
import time

# support
import pyre

# the unit of time
from pyre.units.SI import second

# the size of the staff
members = 8
# how long it may take for every member to be gone; dismissing them one at a time, each after
# the exit of the one before is reported, took about a tenth of a second per member, i.e.
# twice this
allowance = members * 0.05


# a staff that keeps track of its departures
class Staff(pyre.nexus.staff(), family="tests.pyre.nexus.forkserver.standdown.staff"):
    """
    A staff that records when each of its members is gone, and stops its event loop once all of
    them are
    """

    # team obligations
    @pyre.export
    def departed(self, crew, status):
        """
        The process of the {crew} member is gone
        """
        # record when
        self.departures[crew.pid] = time.monotonic()
        # once everybody has left
        if len(self.departures) == members:
            # stop the event loop
            self.dispatcher.stop()
        # all done
        return self

    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # when each member left, by pid
        self.departures = {}
        # all done
        return


# a well behaved task
class Echo(pyre.nexus.task):
    """
    A task with a recognizable result
    """

    # interface
    def execute(self, **kwds):
        """
        The body of the functor
        """
        # hand back a marker
        return "echo"


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


# the application
class StandDown(pyre.application, family="tests.pyre.nexus.forkserver.standdown"):
    """
    An application that recruits a staff through the forkserver and stands it down
    """

    # interface
    @pyre.export
    def main(self, *args, **kwds):
        """
        The main entry point
        """
        # build a staff that recruits through the forkserver
        staff = Staff(name="test.forkserver.standdown")
        staff.size = members
        staff.recruiter = pyre.nexus.forkserver()
        # the outcome drop box
        outcomes = []

        # the passive delivery callback
        def record(result, error):
            """
            Record the outcome; leave the loop running
            """
            # file the report
            outcomes.append((result, error))
            # all done
            return

        # the alarm that winds down the event loop
        def expire(timestamp):
            """
            Stop the event loop
            """
            # ask the dispatcher to stop
            staff.dispatcher.stop()
            # and do not reschedule
            return None

        # give the staff some work
        staff.assign(task=Echo(), callback=record)
        # and let every member check in, finish the work, and get parked
        staff.dispatcher.alarm(interval=2 * second, call=expire)
        staff.dispatcher.watch()
        # the task was delivered
        assert outcomes == [("echo", None)], outcomes
        # and every member is parked
        assert len(staff.idle) == members, len(staff.idle)
        # note who they are
        pids = [crew.pid for crew in staff.idle]

        # stand down, and time it
        start = time.monotonic()
        staff.standDown()
        elapsed = time.monotonic() - start
        # nobody waited for the members
        assert elapsed < 0.1, f"standing down {members} members took {elapsed:.3f} s"
        # and they are off the rosters
        assert not list(staff.crews())
        # in case something goes wrong, give up after a while
        staff.dispatcher.alarm(interval=5 * second, call=expire)
        # let the event loop see them leave
        staff.dispatcher.watch()
        # every member went home
        assert len(staff.departures) == members, staff.departures
        assert all(gone(pid) for pid in pids)
        # promptly
        last = max(staff.departures.values()) - start
        assert last < allowance, f"the last of {members} members left after {last:.3f} s"

        # send the staff home for good
        staff.disband()
        # and ask the helper to leave
        pyre.nexus.forkserver().stop()

        # all done
        return 0


# main
if __name__ == "__main__":
    # instantiate
    app = StandDown(name="forkserver_standdown")
    # invoke
    status = app.run()
    # and share the status with the shell
    raise SystemExit(status)


# end of file
