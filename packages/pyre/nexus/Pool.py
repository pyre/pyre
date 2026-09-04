# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import functools
import os

# support
import pyre
import journal

# base class
from .Peer import Peer

# my protocol
from .Team import Team

# my user configurable state
from .Recruiter import Recruiter


# declaration
class Pool(Peer, family="pyre.nexus.teams.pool", implements=Team):
    """
    A process collective that coöperate to carry out a work plan
    """

    # types
    from .Crew import Crew as crew

    # user configurable state
    size = pyre.properties.int(default=1)
    size.doc = "the number of crew members to recruit"

    recruiter = Recruiter()
    recruiter.doc = "the strategy for recruiting crew members"

    # interface
    @pyre.export
    def assemble(self, workplan, **kwds):
        """
        Assemble a team to execute the set of tasks in my {workplan}
        """
        # grab a journal channel
        channel = self.debug
        # show me
        channel.line("executing the workplan")
        channel.line("  current outstanding tasks: {}".format(len(self.workplan)))
        channel.line("  max team size: {}".format(self.size))
        channel.line("  current vacancies: {}".format(self.vacancies()))
        channel.line("  registered crew members: {}".format(len(self.registered)))
        channel.line("  active crew members: {}".format(len(self.active)))

        # add the new tasks to the workplan
        self.workplan |= workplan
        # tell me
        channel.line("extending the workplan")
        channel.line("  current outstanding tasks: {}".format(len(self.workplan)))

        # if necessary, recruit some new crew members
        self.recruit()
        # tell me
        channel.line("recruited new crew members")
        channel.line("  registered crew members: {}".format(len(self.registered)))
        channel.line("  active crew members: {}".format(len(self.active)))

        # flush
        channel.log()

        # all done
        return self

    @pyre.export
    def overhear(self, crew, record):
        """
        A journal {record} has arrived from {crew}

        The default is to replay it into my own journal, so the entries of every member reach
        the same devices as mine, attributed to the process that produced them
        """
        # replay it
        journal.replay(record=record)
        # all done
        return

    @pyre.export
    def vacancies(self):
        """
        Compute how many recruits are needed to take the team to full strength
        """
        # get the current team size
        current = len(self.registered) + len(self.active)
        # get my pool size limit
        pool = self.size
        # figure out how much work is left to do
        tasks = len(self.workplan)

        # compute the number of vacancies
        return min(tasks, pool) - current

    # meta-methods
    def __init__(self, crew=None, **kwds):
        # chain up
        super().__init__(**kwds)

        # if i were given a non-trivial crew factory
        if crew is not None:
            # attach it
            self.crew = crew

        # initialize my crew registries
        self.registered = set()
        self.active = set()
        self.retired = set()

        # my workplan is the set of tasks that are pending
        self.workplan = set()

        # all done
        return

    # outcome hooks, invoked by crew members as they harvest completion reports
    def collect(self, task, result):
        """
        A crew member has delivered the {result} of {task}
        """
        # a batch pool executes for effect; log the result and move on
        self.debug.log(f"collected {result} from {task}")
        # all done
        return self

    def requeue(self, task, error):
        """
        A crew member reports that {task} failed with a recoverable {error}
        """
        # tell me
        self.debug.log(f"requeueing {task} after {error}")
        # put the task back in the workplan so somebody else gets a crack at it
        self.workplan.add(task)
        # all done
        return self

    def abandon(self, task, error):
        """
        A crew member reports that {task} is permanently lost to {error}
        """
        # log it; the batch completes without this task
        self.debug.log(f"abandoning {task} after {error}")
        # all done
        return self

    def bury(self, crew):
        """
        A {crew} member died without a formal dismissal; clean up after it
        """
        # remove the member from all rosters
        self.registered.discard(crew)
        self.active.discard(crew)
        # carefully
        try:
            # close the team side of its channel
            crew.channel.close()
        # tolerating one that is already gone
        except OSError:
            # nothing further
            pass
        # carefully
        try:
            # reap the corpse
            os.waitpid(crew.pid, 0)
        # tolerating one that was already collected
        except (OSError, ChildProcessError):
            # nothing further
            pass
        # all done
        return self

    # implementation details
    def crews(self):
        """
        Generate the current team members, whatever their state
        """
        # the ones still checking in
        yield from self.registered
        # and the ones that are deployable
        yield from self.active
        # all done
        return

    def recruit(self, **kwds):
        """
        Assemble the team
        """
        # get my recruiter to recruit some workers
        for crew in self.recruiter.recruit(team=self, **kwds):
            # register the crew member
            self.registered.add(crew)
        # all done
        return self

    def activate(self, crew):
        """
        Add the given {crew} member to the scheduling queue
        """
        # upgrade its status from registered
        self.registered.remove(crew)
        # to active
        self.active.add(crew)
        # all done
        return self

    def schedule(self, crew):
        """
        Add the given {crew} member to the execution schedule
        """
        # start sending tasks when the worker is ready to listen
        self.dispatcher.whenWriteReady(
            channel=crew.channel, call=functools.partial(self.submit, crew=crew)
        )
        # all done
        return self

    def submit(self, channel, crew, **kwds):
        """
        A crew member has reported ready to accept tasks
        """
        # N.B.: {channel} is ready to write, because that's how we got here; so write away...

        # tell me
        self.debug.log("sending a task to {.pid}".format(crew))
        # get my workplan
        workplan = self.workplan
        # and my marshaler
        marshaler = self.marshaler

        # if there is nothing left to do
        if not workplan:
            # notify this worker we are done
            self.dismiss(crew=crew)
            # and don't send it any further work
            return False

        # otherwise, grab a task
        task = workplan.pop()
        # and send it to the worker
        crew.execute(team=self, task=task)

        # don't reschedule me; let the handler that harvests the task status decide the fate of
        # this worker
        return False

    def dismiss(self, crew):
        """
        Dismiss the {crew} member from the team
        """
        # notify this crew member it is dismissed
        crew.dismissed()
        # let the recruiter know
        self.recruiter.dismiss(team=self, crew=crew)
        # remove it from the roster
        self.active.discard(crew)
        # and add it to the pile of retired workers
        self.retired.add(crew)
        # all done
        return self

    # private data
    active = None  # the set of currently deployed crew members
    retired = None  # the set of retired crew members


# end of file
