#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the liaison's report handler does not wait on a report channel that was drained
earlier in the same pass of the event loop

Nothing but the report handler reads the report channel on a given event loop, but the readiness
that wakes it is recorded at the start of a pass, and a reader elsewhere, e.g. the report handler
of an event loop nested in a handler that ran earlier in the pass, may take delivery of the
report in between; the handler must leave without waiting for a report that is not coming, and
keep listening for the ones that are
"""

# externals
import signal

# support
import pyre

# the units of the alarm intervals
from pyre.units.SI import second

# the machinery under test
from pyre.nexus.Liaison import Liaison

# what the agency says
from pyre.nexus.messages.Exited import Exited


class Wedged(Exception):
    """
    Exception raised when a pass of the event loop is still running long after it should have
    finished
    """


def expire(signum, frame):
    """
    Interrupt the pass that is still running
    """
    # by raising an exception that the event loop does not handle; the signal must interrupt
    # the handler where it waits, so it bypasses the relay that delivers signals to the loop
    raise Wedged()


def stop(dispatcher):
    """
    Make an alarm that ends the run of {dispatcher} after the pass it comes due in
    """

    # the alarm handler
    def alarm(timestamp):
        """
        End the run
        """
        # ask the loop to stop
        dispatcher.stop()
        # and don't reschedule
        return None

    # hand it off
    return alarm


def run(dispatcher):
    """
    Run a single pass of {dispatcher}, and report whether it finished
    """
    # end the run right after the first pass
    dispatcher.alarm(interval=0 * second, call=stop(dispatcher=dispatcher))
    # a pass that is still running after a few seconds is waiting for something that is not
    # coming
    signal.signal(signal.SIGALRM, expire)
    # so set the deadline
    signal.alarm(5)
    # carefully
    try:
        # run the pass
        dispatcher.watch()
    # if it missed the deadline
    except Wedged:
        # say so
        return False
    # either way
    finally:
        # clear the deadline
        signal.alarm(0)
    # if all went well, the pass finished
    return True


def test():
    # the event loop
    dispatcher = pyre.ipc.newPSL(name="tests.pyre.nexus.liaison.drained.loop")
    # the liaison, with no agency behind it
    liaison = Liaison(name="tests.pyre.nexus.liaison.drained")
    # the report channel; this test plays the agency at the far end
    near, far = pyre.ipc.newSocket().open()
    # hand the liaison its end
    liaison.reports = near
    # and use its marshaler on mine
    marshaler = liaison.marshaler

    # the agency reports that a member is gone
    Exited(pid=101, status=0).send(channel=far, marshaler=marshaler)

    # a reader that takes delivery of the report ahead of the handler, the way the report handler
    # of an event loop nested in an earlier handler would
    def intercept(channel, **kwds):
        """
        Hear the report channel
        """
        # take delivery of the report
        liaison.hear(channel=liaison.reports)
        # and don't do it again
        return False

    # the kernel does not promise the order in which the channels of a pass are served, but the
    # handlers of a channel run in the order they were registered; registering the reader on the
    # report channel ahead of the report handler puts it first in the pass that finds the channel
    # readable
    dispatcher.whenReadReady(channel=near, call=intercept)
    # followed by the report handler, the way the liaison listens
    dispatcher.whenReadReady(channel=near, call=liaison.report)

    # the pass finishes
    assert run(dispatcher=dispatcher), "the report handler waited on a drained channel"
    # and the report was heard, once
    assert liaison.collect(pid=101) == (True, 0)

    # the agency reports another exit
    Exited(pid=303, status=0).send(channel=far, marshaler=marshaler)
    # the next pass finishes
    assert run(dispatcher=dispatcher), "the report handler waited on a drained channel"
    # and the liaison heard the report, so it is still listening
    assert liaison.collect(pid=303) == (True, 0)

    # stop watching
    dispatcher.close()
    # and hang up
    near.close()
    # on both ends
    far.close()

    # all done
    return liaison


# main
if __name__ == "__main__":
    test()


# end of file
