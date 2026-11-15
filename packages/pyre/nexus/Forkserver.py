# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# my superclass
from .Fork import Fork

# the staffing agency's representative in this process
from .Liaison import Liaison

# the request for a member
from .messages.Recruit import Recruit


# declaration
class Forkserver(Fork, family="pyre.nexus.recruiters.forkserver"):
    """
    Create worker processes by asking the staffing agency to fork them

    The agency is a clean copy of the application, spawned from its command line the first time
    it is needed and kept for the life of the process. Crew members are forked by the agency, so
    they inherit the state of the application as it was at startup, and nothing that the team's
    process has done since, e.g. the threads of a library it has used, which do not survive a
    fork and leave a member waiting forever on one that does not exist on its side

    Whatever a member needs that is set after startup has to travel with its tasks, or be sent
    to it: the journal controls a team applies reach the agency too, so the members it forks
    from then on start with them in place. Members leave the way they do under {Fork}, except
    that they are the agency's children, so it is the agency that reports their exits
    """

    # interface
    @classmethod
    def start(cls, dispatcher=None) -> Liaison:
        """
        Make sure the staffing agency is running, and heard on {dispatcher}; applications that
        fork crew members after they have touched libraries with threads of their own start it
        early, before they do
        """
        # ask the liaison
        return Liaison.instance().start(dispatcher=dispatcher)

    @classmethod
    def stop(cls) -> Liaison:
        """
        Send the staffing agency home
        """
        # ask the liaison
        return Liaison.instance().stop()

    # protocol obligations
    @pyre.export
    def deploy(self, team, **kwds):
        """
        Create a new {team} member by asking the staffing agency to fork it
        """
        # the agency forks members with nothing but what it is sent
        if kwds:
            # get the journal
            import journal

            # make a channel
            channel = journal.firewall("pyre.nexus.staffing")
            # complain
            channel.line("the staffing agency cannot build a crew member with arguments")
            channel.line(f"arguments: {sorted(kwds)}")
            # flush
            channel.log()
        # make sure the agency is running, and heard on the team's event loop
        liaison = self.start(dispatcher=team.dispatcher)
        # team members communicate with the manager over my transport; the {child} end is
        # destined for the worker, the {parent} end stays with the team
        parent, child = self.channels.open()
        # the worker's journal entries travel back over a channel of their own, when wanted
        parentJournal, childJournal = self.channels.open() if self.journal else (None, None)
        # ask the agency for a new member of the kind the team employs
        pid = liaison.recruit(request=Recruit(crew=team.crew, channel=child, journal=childJournal))
        # the worker's ends are the agency's business now; release mine
        child.close()
        # and the worker's end of the journal channel, if there is one
        if childJournal is not None:
            # release it
            childJournal.close()
        # make a member proxy for the team manager and return it
        crew = team.crew(pid=pid, channel=parent, journal=parentJournal, timer=team.timer)
        # adjust its support for asynchrony
        crew.dispatcher = team.dispatcher
        # and its message serializer
        crew.marshaler = team.marshaler
        # spin it up and return it
        return crew.join(team=team)

    @pyre.export
    def instruct(self, control):
        """
        Pass the journal {control} to the staffing agency, so the members it forks later start
        with it in place
        """
        # ask the liaison
        Liaison.instance().instruct(control=control)
        # all done
        return

    # implementation details
    def listen(self, dispatcher):
        """
        Hear the exits of my members on {dispatcher}: they are the agency's children, so the
        agency reports them, and its reports arrive on the event loop
        """
        # make sure the agency is heard there
        liaison = self.start(dispatcher=dispatcher)
        # and have it tell me of every exit it reports
        liaison.subscribe(call=self.exited)
        # all done
        return self

    def reap(self, pid):
        """
        Check, without waiting, whether the member {pid} is gone; report whether it is, and its
        exit status
        """
        # the agency collected it, if it is
        return Liaison.instance().collect(pid=pid)


# end of file
