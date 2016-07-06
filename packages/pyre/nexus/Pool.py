# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import functools
# support
import pyre
# base class
from .Peer import Peer
# my protocol
from .Team import Team
# my user configurable state
from .Recruiter import Recruiter


# declaration
class Pool(Peer, family='pyre.nexus.teams.pool', implements=Team):
    """
    A process collective that coöperate to carry out a work plan
    """


    # types
    from .TeamMember import TeamMember as member


    # user configurable state
    size = pyre.properties.int(default=1)
    size.doc = 'the number of team members to recruit'

    recruiter = Recruiter()
    recruiter.doc = 'the strategy for recruiting team members'


    # interface
    @pyre.export
    def execute(self, workplan, **kwds):
        """
        Recruit a team to execute the set of tasks in my {workplan}
        """
        # grab a journal channel
        channel = self.debug
        # show me
        channel.line('executing the workplan')
        channel.line('  current outstanding tasks: {}'.format(len(self.workplan)))
        channel.line('  max team size: {}'.format(self.size))
        channel.line('  current vacancies: {}'.format(self.vacancies()))
        channel.line('  active team members: {}'.format(len(self.active)))

        # add the new tasks to the workplan
        self.workplan |= workplan
        # tell me
        channel.line('extending the workplan')
        channel.line('  current outstanding tasks: {}'.format(len(self.workplan)))

        # if necessary, recruit some new team members
        self.recruit()
        # tell me
        channel.line('recruiting new team member')
        channel.line('  active team members: {}'.format(len(self.active)))

        # flush
        channel.log()

        # all done
        return self


    @pyre.export
    def vacancies(self):
        """
        Compute how may recruits are needed to take the team to full strength
        """
        # get the current team size
        active = len(self.active)
        # get my pool size limit
        pool = self.size
        # figure out how much work is left to do
        tasks = len(self.workplan)

        # compute the number of vacancies
        return min(tasks, pool) - active


    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)

        # initialize my records
        self.active = set()
        self.retired = set()

        # my workplan is a the set of tasks that are pending
        self.workplan = set()

        # all done
        return


    # implementation details
    def recruit(self):
        """
        Assemble the team
        """
        # get my recruiter to recruit some workers
        for teamMember in self.recruiter.recruit(team=self):
            # activate and register
            self.activate(member=teamMember)
        # all done
        return self


    def activate(self, member):
        """
        Add the given {member} to the scheduling queue
        """
        # start sending tasks when the worker is ready to listen
        self.dispatcher.whenWriteReady(
            channel = member.channel,
            call = functools.partial(self.schedule, member=member))
        # add it to the active pile
        self.active.add(member)
        # all done
        return self


    def schedule(self, channel, member, **kwds):
        """
        A team member has reported ready to accept tasks
        """
        # N.B.: {channel} is ready to write, because that's how we got here; so write away...

        # tell me
        self.debug.log('sending a task to {.pid}'.format(member))
        # get my workplan
        workplan = self.workplan
        # and my marshaler
        marshaler = self.marshaler

        # if there is nothing left to do
        if not workplan:
            # notify this worker we are done
            self.dismiss(member=member)
            # and don't send it any further work
            return False

        # otherwise, grab a task
        task = workplan.pop()
        # and send it to the worker
        member.execute(team=self, task=task)

        # don't reschedule me; let the handler that harvests the task status decide the fate of
        # this worker
        return False


    def welcome(self, member):
        """
        The recruiter has identified a new team member
        """
        # nothing to do, by default
        return self


    def dismiss(self, member):
        """
        Dismiss the {member} from the team
        """
        # notify this team member it is dismissed
        member.dismissed()
        # let the recruiter know
        self.recruiter.dismiss(team=self, member=member)
        # remove it from the roster
        self.active.discard(member)
        # and add it to the pile of retured workers
        self.retired.add(member)
        # all done
        return self


    # private data
    active = None   # the set of currently deployed team members
    retired = None  # the set of retired team members


# end of file
