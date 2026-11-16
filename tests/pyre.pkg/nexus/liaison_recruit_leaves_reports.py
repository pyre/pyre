#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a recruitment reads its answer from the control channel and leaves the agency's
reports of exits to the report handler, even when a report is waiting as the recruitment runs
"""

# externals
import os

# support
import pyre

# the units of the alarm intervals
from pyre.units.SI import second

# the machinery under test
from pyre.nexus.Liaison import Liaison

# what the agency says
from pyre.nexus.messages.Exited import Exited
from pyre.nexus.messages.Recruited import Recruited

# and the request it answers
from pyre.nexus.messages.Recruit import Recruit


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


def test():
    # the event loop
    dispatcher = pyre.ipc.newPSL(name="tests.pyre.nexus.liaison.reports.loop")
    # the liaison, with no agency behind it
    liaison = Liaison(name="tests.pyre.nexus.liaison.reports")
    # the control channel, whose far end this test holds in place of the agency
    control, agencyControl = pyre.ipc.newSocket().open()
    # and the report channel, whose far end it holds as well
    reports, agencyReports = pyre.ipc.newSocket().open()
    # hand the liaison its ends
    liaison.control = control
    liaison.reports = reports
    # and use its marshaler on mine
    marshaler = liaison.marshaler

    # the member the report is about: a process that exists, so the liaison, which has no agency
    # to ask, does not take it for gone before it hears the report
    member = os.getpid()
    # the agency reports that it is gone
    Exited(pid=member, status=0).send(channel=agencyReports, marshaler=marshaler)
    # and the answer to the recruitment that is about to happen is ready too
    Recruited(pids=[202, 203]).send(channel=agencyControl, marshaler=marshaler)

    # the channel of one new member
    oneTeam, oneMember = pyre.ipc.newSocket().open()
    # and of the other
    otherTeam, otherMember = pyre.ipc.newSocket().open()
    # recruit them
    pids = liaison.recruit(request=Recruit(crew=pyre.nexus.crew, channels=[oneMember, otherMember]))
    # the recruitment got its answer
    assert pids == [202, 203]
    # and left the report alone
    assert liaison.collect(pid=member) == (False, None)

    # the report handler hears the report channel on the event loop
    dispatcher.whenReadReady(channel=reports, call=liaison.report)
    # arrange for the loop to stop after a single pass
    dispatcher.alarm(interval=0 * second, call=stop(dispatcher=dispatcher))
    # and run it
    dispatcher.watch()
    # the report was delivered there
    assert liaison.collect(pid=member) == (True, 0)

    # stop watching
    dispatcher.close()
    # and hang up
    for channel in (
        control,
        agencyControl,
        reports,
        agencyReports,
        oneTeam,
        oneMember,
        otherTeam,
        otherMember,
    ):
        # one at a time
        channel.close()

    # all done
    return liaison


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
