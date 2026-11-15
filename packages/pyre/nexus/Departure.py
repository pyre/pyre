# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import os
import signal


# declaration
class Departure:
    """
    A crew member on its way out: the team it served, when it is next due to be gone, and the
    reminders it gets if it is not

    A member is expected to leave on its own, and gets a grace period to do so. One that is still
    around when the period is over is told to go, and one that ignores that is removed: a team
    must never wait on a member, since the team lives in the process that serves everybody else,
    and a member stuck on its way out, e.g. in an exit handler that waits for a thread that does
    not exist on its side of the fork, would otherwise hold that process hostage
    """

    # interface
    def due(self, now: float) -> bool:
        """
        Check whether the member should have been gone by {now}
        """
        # easy enough
        return now >= self.deadline

    def remind(self, now: float, grace: float) -> "Departure":
        """
        Send the member the next reminder, if it has one coming, and give it another {grace}
        seconds from {now}
        """
        # if there is a reminder left
        if self.reminders:
            # take the next one, from polite to final
            reminder = self.reminders.pop(0)
            # get the journal
            import journal

            # say what is about to happen
            journal.debug("pyre.nexus.departures").log(
                f"{self.team.pyre_name}: member {self.crew.pid} is late; "
                f"sending {signal.Signals(reminder).name}"
            )
            # carefully
            try:
                # send it
                os.kill(self.crew.pid, reminder)
            # if the member is already gone
            except ProcessLookupError:
                # its exit is about to be collected, so there is nobody to remind
                pass
        # either way, look again once the new period is over; a member that ignored every
        # reminder is past its last one, and only its exit is left to collect
        self.deadline = now + grace
        # all done
        return self

    # metamethods
    def __init__(self, crew, team, deadline: float, **kwds):
        # chain up
        super().__init__(**kwds)
        # the member
        self.crew = crew
        # the team it served, which is told when it is gone
        self.team = team
        # when it is next due to be gone
        self.deadline = deadline
        # and the reminders it gets if it is not, from polite to final
        self.reminders = [signal.SIGTERM, signal.SIGKILL]
        # all done
        return


# end of file
