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
    def recruit(self, team, **kwds):
        """
        Recruit members for the {team}, filling all its vacancies in as few requests to the
        staffing agency as its control channel can carry
        """
        # the agency forks members with nothing but what it is sent
        self.refuse(arguments=kwds)
        # fill the vacancies
        yield from self.enlist(team=team, count=team.vacancies())
        # all done
        return

    @pyre.export
    def deploy(self, team, **kwds):
        """
        Create a new {team} member by asking the staffing agency to fork it
        """
        # the agency forks members with nothing but what it is sent
        self.refuse(arguments=kwds)
        # recruit one
        (crew,) = self.enlist(team=team, count=1)
        # and hand it off
        return crew

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
    def enlist(self, team, count):
        """
        Generate {count} new members of {team}, forked by the staffing agency in as few requests
        as its control channel can carry
        """
        # make sure the agency is running, and heard on the team's event loop
        liaison = self.start(dispatcher=team.dispatcher)
        # until every member is recruited
        while count > 0:
            # the ends of the first member of the next request
            first = self.ends()
            # the descriptors it takes to the agency
            descriptors = sum(len(end.descriptors()) for end in first[1::2] if end is not None)
            # how many members a request has room for, judging by the first one
            room = max(1, liaison.control.capacity // descriptors)
            # the ends of all the members of the request
            members = [first] + [self.ends() for _ in range(min(count, room) - 1)]
            # make the request: the kind of member the team employs, and the member's ends of
            # the channels of each of them
            request = Recruit(
                crew=team.crew,
                channels=[child for _, child, _, _ in members],
                journals=[childJournal for _, _, _, childJournal in members],
            )
            # and ask the agency for them
            pids = liaison.recruit(request=request)
            # the members' ends are the agency's business now
            for _, child, _, childJournal in members:
                # so release mine
                child.close()
                # and the member's end of its journal channel, if there is one
                if childJournal is not None:
                    # release it
                    childJournal.close()
            # the members the agency did not fork, if it answered for fewer of them
            for parent, _, parentJournal, _ in members[len(pids) :]:
                # have nobody on the other end
                parent.close()
                # of either channel
                if parentJournal is not None:
                    # so release my ends too
                    parentJournal.close()
            # go through the members that were forked
            for pid, (parent, _, parentJournal, _) in zip(pids, members):
                # make a member proxy for the team manager
                crew = team.crew(pid=pid, channel=parent, journal=parentJournal, timer=team.timer)
                # adjust its support for asynchrony
                crew.dispatcher = team.dispatcher
                # and its message serializer
                crew.marshaler = team.marshaler
                # spin it up and hand it off
                yield crew.join(team=team)
            # if the agency answered for fewer members than were asked for
            if len(pids) < len(members):
                # it will not do better on another try
                break
            # account for the ones recruited
            count -= len(members)
        # all done
        return

    def ends(self) -> tuple:
        """
        Open the channels of a new member: the one it talks to its team over and, when its
        journal is routed back, the one its journal travels over; the {parent} ends stay with
        the team, the {child} ends go to the member
        """
        # team members communicate with the manager over my transport
        parent, child = self.channels.open()
        # the member's journal entries travel back over a channel of their own, when wanted
        parentJournal, childJournal = self.channels.open() if self.journal else (None, None)
        # hand them off
        return parent, child, parentJournal, childJournal

    def refuse(self, arguments: dict) -> "Forkserver":
        """
        Complain about the {arguments} of a recruitment: the agency forks members with nothing
        but what it is sent
        """
        # if there are none
        if not arguments:
            # there is nothing to complain about
            return self
        # get the journal
        import journal

        # make a channel
        channel = journal.firewall("pyre.nexus.staffing")
        # complain
        channel.line("the staffing agency cannot build a crew member with arguments")
        # and name the arguments
        channel.line(f"arguments: {sorted(arguments)}")
        # flush
        channel.log()
        # all done
        return self

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
