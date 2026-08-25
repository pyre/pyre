# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import os

# support
import pyre

# my protocol
from .Recruiter import Recruiter


# declaration
class Fork(pyre.component, family="pyre.nexus.recruiters.fork", implements=Recruiter):
    """
    Create worker processes by cloning the current one

    New team members inherit only what they need: each side of the crew channel closes the end
    it does not own, so a worker sees end-of-file when the team dies instead of lingering on a
    channel its own inherited copies hold open; and workers shed everything else the fork
    handed them that is none of their business, i.e. whatever the shared event loop watches
    and the channels of the crews deployed before them
    """

    # user configurable state
    channels = pyre.ipc.transport()
    channels.doc = "the ipc mechanism that connects the team to its crew members"

    # protocol obligations
    @pyre.provides
    def recruit(self, team, **kwds):
        """
        Recruit members for the {team}
        """
        # compute the number of vacancies in the team
        vacancies = team.vacancies()
        # recruit the right number of team members
        for _ in range(vacancies):
            # deploy them and add them to the team
            yield self.deploy(team=team, **kwds)
        # all done
        return

    @pyre.provides
    def deploy(self, team, **kwds):
        """
        Create a new {team} member using the {fork} system call
        """
        # team members communicate with the manager over my transport; the {child} end is
        # destined for the worker, the {parent} end stays with the team
        parent, child = self.channels.open()
        # clone the current process
        pid = os.fork()

        # N.B.: it is important that the worker side of a new team member gets a fresh event
        # loop manager, while the team side is tied to the shared one.

        # in the worker process
        if pid == 0:
            # the team's end is not mine to hold; release my inherited copy so the channel
            # closes for real when the team side lets go
            parent.close()
            # shed the rest of the connections the fork handed me
            self.shed(team=team)
            # make a team member
            crew = team.crew(pid=os.getpid(), channel=child, **kwds)
            # ask it to register with the team
            crew.register()
            # spin up and carry out tasks until there is nothing more to do
            status = crew.run()
            # at which point, this process must terminate
            raise SystemExit(status)

        # on the team side, release the worker's end for the same reason
        child.close()
        # make a member proxy for the team manager and return it
        crew = team.crew(pid=pid, channel=parent, timer=team.timer)
        # adjust its support for asynchrony
        crew.dispatcher = team.dispatcher
        # and its message serializer
        crew.marshaler = team.marshaler
        # spin it up and return it
        return crew.join(team=team)

    @pyre.provides
    def dismiss(self, team, crew, **kwds):
        """
        The {team} manager has dismissed the given {member}
        """
        # harvest the status
        status = os.waitpid(crew.pid, 0)
        # all done
        return

    # implementation details
    def shed(self, team):
        """
        Close the inherited connections that belong to the {team} side, not to a new crew
        member

        The parent's open data files are left alone deliberately: closing their descriptors
        out from under the inherited objects that will finalize them invites descriptor reuse
        bugs, and holding them is harmless
        """
        # collect the channels the shared event loop is watching
        pile = set(team.dispatcher.channels())
        # add the channels of every deployed crew; members between tasks may have no armed
        # handler, so the event loop does not know about them
        pile |= set(crew.channel for crew in team.crews())
        # go through the pile
        for channel in pile:
            # carefully, since a descriptor may already be gone
            try:
                # release my inherited copy
                channel.close()
            # dead ones
            except OSError:
                # need nothing further
                continue
        # all done
        return


# end of file
