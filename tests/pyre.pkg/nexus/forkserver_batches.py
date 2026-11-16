#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a staff too large for one request to the staffing agency is recruited in several:
every member is forked, checks in, and gets parked, each under a pid of its own
"""

# support
import pyre

# the units of the alarm intervals
from pyre.units.SI import second

# the recruiter, and the channel its requests travel over
from pyre.nexus.Forkserver import Forkserver
from pyre.ipc.SocketPair import SocketPair

# over the socket transport, a member with its journal routed back takes a descriptor for each of
# its two channels, so one more than a request has room for needs two requests
members = SocketPair.capacity // 2 + 1


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


# the application
class Batches(pyre.application, family="tests.pyre.nexus.forkserver.batches"):
    """
    An application that recruits a large staff through the forkserver
    """

    # interface
    @pyre.export
    def main(self, *args, **kwds):
        """
        The main entry point
        """
        # build a staff that recruits through the forkserver, over the socket transport, with the
        # journals of its members routed back
        staff = pyre.nexus.staff()(name="test.forkserver.batches")
        staff.size = members
        staff.recruiter = pyre.nexus.forkserver()
        staff.recruiter.channels = pyre.ipc.newSocket()
        staff.recruiter.journal = True
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

        # give the staff some work, which recruits it
        staff.assign(task=Echo(), callback=record)
        # and let every member check in, finish the work, and get parked
        staff.dispatcher.alarm(interval=4 * second, call=expire)
        # by turning the event loop
        staff.dispatcher.watch()
        # the task was delivered
        assert outcomes == [("echo", None)], outcomes
        # every member is parked
        assert len(staff.idle) == members, len(staff.idle)
        # each under a pid of its own
        assert len({crew.pid for crew in staff.idle}) == members

        # send everybody home
        staff.disband()
        # and the staffing agency too
        Forkserver.stop()

        # all done
        return 0


# main
if __name__ == "__main__":
    # instantiate
    app = Batches(name="forkserver_batches")
    # invoke
    status = app.run()
    # and share the status with the shell
    raise SystemExit(status)


# end of file
