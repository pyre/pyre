# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


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
class Pool(Peer, family="pyre.nexus.teams.pool", implements=Team):
    """
    A process collective that coöperate to carry out a work plan
    """

    # types
    from .Crew import Crew as crew

    # user configurable state
    size = pyre.properties.int()
    size.default = 1
    size.doc = "the number of crew members to recruit"

    # how often a task may fail before i give up on it
    retries = pyre.properties.int()
    retries.default = 3
    retries.doc = (
        "the number of times a task that fails with a recoverable error is tried again before "
        "it is abandoned"
    )

    # how my members are recruited
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
        # show me what is about to happen
        channel.line("executing the workplan")
        # how much work is waiting
        channel.line(f"  current outstanding tasks: {len(self.workplan)}")
        # how many members the team may have
        channel.line(f"  max team size: {self.size}")
        # how many of them are missing
        channel.line(f"  current vacancies: {self.vacancies()}")
        # how many are checking in
        channel.line(f"  registered crew members: {len(self.registered)}")
        # and how many are at work
        channel.line(f"  active crew members: {len(self.active)}")

        # add the new tasks to the workplan
        self.workplan |= workplan
        # tell me
        channel.line("extending the workplan")
        # how much work is waiting now
        channel.line(f"  current outstanding tasks: {len(self.workplan)}")

        # if necessary, recruit some new crew members
        self.recruit()
        # tell me
        channel.line("recruited new crew members")
        # how many are checking in now
        channel.line(f"  registered crew members: {len(self.registered)}")
        # and how many are at work
        channel.line(f"  active crew members: {len(self.active)}")

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
        # get the journal; imported here because the package boots the framework, which
        # imports me
        import journal

        # replay it
        journal.replay(record=record)
        # all done
        return

    @pyre.export
    def instruct(self, control):
        """
        Apply the {control} instruction to my own journal, and send it to every crew member

        The members already deployed are told directly; my recruiter is told as well, so the
        members it recruits from now on start with the new state, whether they inherit it or
        have to be sent it
        """
        # apply it here
        control.apply()
        # tell my recruiter
        self.recruiter.instruct(control=control)
        # go through the members
        for crew in self.crews():
            # carefully, since a member may have died
            try:
                # tell each one
                crew.instruct(control=control)
            # a dead member raises while being written to
            except OSError:
                # nothing more to do for it
                continue
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
        # and the recoverable failures of the tasks that have had any
        self.failures = {}

        # all done
        return

    # outcome hooks, invoked by crew members as they harvest completion reports
    def collect(self, task, result):
        """
        A crew member has delivered the {result} of {task}
        """
        # the task is done, so its failures no longer count
        self.failures.pop(task, None)
        # nothing to do with the {result} of the {task}, but if someone is listening
        if self.debug.active:
            # let them know the {task} is complete
            self.debug.log(f"collected {result} from {task}")
        # all done
        return self

    def requeue(self, task, error):
        """
        A crew member reports that {task} failed with a recoverable {error}

        The task goes back in my workplan, unless it has already been tried again as many times
        as my {retries} allow, in which case it is abandoned with this {error}
        """
        # count this failure
        failures = self.failures.get(task, 0) + 1
        # if the task has used up its retries
        if failures > self.retries:
            # give up on it, with the last error
            return self.abandon(task=task, error=error)
        # otherwise, remember how often it has failed
        self.failures[task] = failures
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
        # the task is gone, so its failures no longer count
        self.failures.pop(task, None)
        # log it; the batch completes without this task
        self.debug.log(f"abandoning {task} after {error}")
        # all done
        return self

    def bury(self, crew):
        """
        A {crew} member died without a formal dismissal; clean up after it
        """
        # get the journal
        import journal

        # say what happened
        journal.debug("pyre.nexus.departures").log(
            f"{self.pyre_name}: member {crew.pid} died without being dismissed"
        )
        # take the member off the roster of the ones checking in
        self.registered.discard(crew)
        # and off the one of the ones at work
        self.active.discard(crew)
        # carefully
        try:
            # close the team side of its channel
            crew.channel.close()
        # tolerating one that is already gone
        except OSError:
            # nothing further
            pass
        # its process is my recruiter's to collect, since only it knows whose child it is
        self.recruiter.bury(team=self, crew=crew)
        # all done
        return self

    @pyre.export
    def departed(self, crew, status):
        """
        The process of the {crew} member is gone, with the exit {status} my recruiter collected

        A pool has taken the member off its rosters already, when it dismissed or buried it, so
        there is nothing left to do; teams that care how their members left override this
        """
        # nothing to do
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
        # get the journal; imported here because the package boots the framework, which
        # imports me
        import journal

        # make a channel
        channel = journal.debug("pyre.nexus.recruitment")
        # get my recruiter to recruit some workers
        for crew in self.recruiter.recruit(team=self, **kwds):
            # register the crew member
            self.registered.add(crew)
            # and say so
            channel.log(f"{self.pyre_name}: recruited member {crew.pid}")
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
        # get the journal
        import journal

        # and say that it checked in
        journal.debug("pyre.nexus.recruitment").log(
            f"{self.pyre_name}: member {crew.pid} checked in"
        )
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
        # get the journal
        import journal

        # say what is happening
        journal.debug("pyre.nexus.departures").log(f"{self.pyre_name}: dismissed member {crew.pid}")
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
    failures = None  # the number of recoverable failures of each task that has had any


# end of file
