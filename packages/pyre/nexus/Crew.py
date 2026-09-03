# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import functools
import os
import signal

# the unit the task deadline is expressed in
from ..units.SI import second

# the marker the marshaler raises when its peer dies mid-conversation
from ..ipc.exceptions import EndOfStream

# the marker for tasks that took their crew member down
from .exceptions import Casualty

# my base class
from .Peer import Peer


# declaration
class Crew(Peer, family="pyre.nexus.peers.crew"):
    """
    The base facilitator of asynchronous task execution in foreign processes, and one of the
    building blocks of process based concurrency in pyre.

    Crew members are typically instantiated by a {recruiter} in matching pairs that are
    connected to each other via bidirectional {channels}. One member of the pair participates
    in the event logic of the host application; this instance is referred to as the team side
    crew member. The other is hosted by a remote pyre {shell} with its own event loop, and is
    referred to as the worker side. Making the worker side functional typically involves
    spinning up a new process, but this is considered a {recruiter} implementation detail. The
    pair of crew instances are responsible only for the babysitting of the task execution.

    The team side crew member acts as a proxy for the worker side. The host application
    schedules the execution of a {task} by invoking the team side interface. The crew instance
    serializes the task and sends it off to its remote twin for execution, monitors progress,
    and reports the task result back to the host application.
    """

    # types
    from .exceptions import RecoverableError
    from .CrewStatus import CrewStatus as crewcodes
    from .TaskStatus import TaskStatus as taskcodes

    # interface - team side
    def join(self, team):
        """
        Join a team

        This is invoked by my recruiter on the team side and it is part of team assembly. The
        intent is to make crew members available to the team after they have reported ready to
        receive tasks for execution
        """
        # schedule the handler of the worker side registration
        self.dispatcher.whenReadReady(
            channel=self.channel, call=functools.partial(self.activate, team=team)
        )
        # all done
        return self

    def activate(self, channel, team):
        """
        My worker twin is reporting ready to work

        N.B.: this is an event handler; careful with its return value
        """
        # check it's me we are talking about
        assert channel is self.channel
        # carefully, since my twin may have died before its registration arrived
        try:
            # get the status of my twin
            status = self.marshaler.recv(channel=channel)
        # if the channel delivered a truncated message, my twin is gone
        except EndOfStream:
            # clean up; the team decides whether a replacement gets recruited
            team.bury(crew=self)
            # and stop listening
            return False
        # if all is good
        if status is self.crewcodes.healthy:
            # let the team know
            team.activate(crew=self)
            # and add me to the execution schedule
            team.schedule(crew=self)
        # otherwise
        else:
            # my twin is compromised; clean up, rather than leaking it in the roster
            team.bury(crew=self)
        # do not reschedule this handler
        return False

    def execute(self, team, task):
        """
        Send my twin the {task} to be executed
        """
        # remember what my twin is working on, so a deadline that fires later can tell
        # whether it is still waiting on this task or on something that came after
        self.task = task
        # send the task
        self.marshaler.send(channel=self.channel, item=task)
        # schedule the harvesting of the result
        self.dispatcher.whenReadReady(
            channel=self.channel, call=functools.partial(self.assess, team=team, task=task)
        )
        # a team that puts a limit on how long a task may take
        patience = getattr(team, "patience", None)
        # arms a deadline; a limit of zero is a team willing to wait indefinitely, which is
        # the default, and a quantity of zero is not falsy, so ask rather than assume
        if patience is not None and patience > 0 * second:
            # so a twin that never answers cannot hold the queue behind it forever
            self.dispatcher.alarm(
                interval=patience,
                call=functools.partial(self.overdue, team=team, task=task),
            )
        # all done
        return self

    def overdue(self, timestamp, team, task):
        """
        The deadline for {task} has passed with no report

        N.B.: this is an alarm handler; returning {None} keeps it from being rescheduled
        """
        # if this is not what my twin is working on any more, the report arrived in time and
        # the deadline is moot
        if self.task is not task:
            # so there is nothing to do
            return None
        # otherwise my twin has had long enough. whatever it is doing, nobody is going to
        # wait on it any longer: hand the requester an answer it can act on, rather than
        # leaving it holding a promise that may never be kept
        self.task = None
        team.abandon(
            task=task,
            error=self.RecoverableError(description=f"crew {self.pid} took too long"),
        )
        # my twin is still running, and it is exactly the kind of process that may never
        # stop. a burial waits for a corpse rather than making one, so handing it a live
        # worker would block the event loop until that worker decided to finish -- which is
        # the very thing we have just declared it cannot be trusted to do. so end it first
        try:
            # with prejudice; a member that has blown its deadline gets no chance to object
            os.kill(self.pid, signal.SIGKILL)
        # tolerating one that has already gone on its own
        except (OSError, ProcessLookupError):
            # nothing further
            pass
        # and now clean up after it: the burial closes the channel, reaps the corpse -- which
        # returns at once, since there is one -- takes it off the rosters, and lets the team
        # recruit a replacement
        team.bury(crew=self)
        # do not reschedule
        return None

    def assess(self, channel, team, task, **kwds):
        """
        Harvest the task completion status
        """
        # carefully, since my twin may have died mid-task instead of reporting
        try:
            # grab the report
            memberstatus, taskstatus, result = self.harvest(channel=channel)
        # if the channel delivered a truncated message, my twin is gone
        except EndOfStream:
            # a death without a report marks the task as a suspect
            team.abandon(task=task, error=Casualty(description=f"crew {self.pid} died"))
            # clean up; the team decides whether a replacement gets recruited
            team.bury(crew=self)
            # and stop listening
            return False
        # my twin has answered for this task, so any deadline still standing over it is moot
        self.task = None
        # show me on the debug channel
        self.debug.log(f"{self.pid}: {memberstatus}, {taskstatus}, {result}")

        # first, let's figure out what to do with the task. the delivery runs code that
        # belongs to whoever asked for the task, and it may fail; my own fate must be
        # settled regardless, or a failed subscriber leaves me counted as busy with nobody
        # listening to me, and the team never hands out work again
        try:
            # if it ran to completion
            if taskstatus is self.taskcodes.completed:
                # deliver the result; the team decides what results are for
                team.collect(task=task, result=result)
            # if it failed due to some temporary condition
            elif taskstatus is self.taskcodes.failed:
                # tell me
                self.reportRecoverableError(team=team, task=task, error=result)
                # the team decides whether it gets another chance
                team.requeue(task=task, error=result)
            # otherwise, the task aborted
            else:
                # deliver the bad news; the team decides how to break it
                team.abandon(task=task, error=result)
        # whatever the delivery did
        finally:
            # now, let's figure out what to do with me; if i'm healthy
            if memberstatus is self.crewcodes.healthy:
                # put me back in the work queue
                team.schedule(crew=self)
            # otherwise
            else:
                # tell me
                self.reportUnrecoverableError(team=team, task=task, error=result)
                # dismiss me
                team.dismiss(crew=self)

        # all done
        return False

    def harvest(self, channel):
        """
        Extract a completion report from {channel}

        Subclasses whose reports have trailers, e.g. payloads that travel outside the
        marshaled byte stream, override this to collect them
        """
        # pull the report from the channel
        return self.marshaler.recv(channel=channel)

    def dismissed(self):
        """
        My team manager has dismissed me
        """
        # send the end-of-tasks marker
        self.marshaler.send(channel=self.channel, item=None)
        # clean up
        self.resign()
        # leave a note
        self.debug.log(f"{self.pid}: dismissed at {self.finish:.3f}")
        # all done
        return self

    def reportRecoverableError(self, team, task, error):
        """
        Report a task failure that can be reasonably expected to be temporary
        """
        # show me
        self.debug.log(f"{self.pid}: recoverable error: {error}")
        # all done
        return

    def reportUnrecoverableError(self, team, task, error):
        """
        Report a permanent task failure
        """
        # show me
        self.debug.log(f"{self.pid}: unrecoverable error: {error}")
        # all done
        return

    # interface - worker side
    def register(self):
        """
        Initialize the worker side
        """
        # send in my registration when the write side of my channel is ready to accept data
        self.dispatcher.whenWriteReady(channel=self.channel, call=self.checkin)
        # and chain up to start processing events
        return self

    def checkin(self, channel):
        """
        Send my team registration now that my communication channel is open
        """
        # check it's me we are talking about
        assert channel is self.channel
        # send in a healthy status code
        self.marshaler.send(channel=channel, item=self.crewcodes.healthy)
        # register the task execution handler
        self.dispatcher.whenReadReady(channel=self.channel, call=self.perform)
        # do not reschedule this handler
        return False

    def perform(self, channel, **kwds):
        """
        A notification has arrived that indicates there is a task waiting to be executed
        """
        # carefully, since a broken channel means the team is gone
        try:
            # extract the task from the channel
            task = self.marshaler.recv(channel=channel)
        # if the channel delivered a truncated message
        except EndOfStream:
            # wind down my event loop
            self.stop()
            # and stop listening
            return False
        # leave a note
        self.debug.log(f"{self.pid}: got {task}")
        # if it's a quit marker
        if task is None:
            # we are all done
            self.stop()
            # don't reschedule this handler
            return False

        # otherwise, try to
        try:
            # execute the task and collect its result
            result = self.engage(task=task, **kwds)
        # if the task failure is recoverable
        except self.RecoverableError as error:
            # prepare a report with an error code for the task
            taskstatus = self.taskcodes.failed
            # a clean bill of health for me
            crewstatus = self.crewcodes.healthy
            # and attach the error description
            result = error
        # if anything else goes wrong
        except Exception as error:
            # prepare a report with an error code for the task
            taskstatus = self.taskcodes.aborted
            # mark me as damaged
            crewstatus = self.crewcodes.damaged
            # and attach the error description
            result = error
        # if all goes well
        else:
            # indicate task success
            taskstatus = self.taskcodes.completed
            # and a clean bill of health for me
            crewstatus = self.crewcodes.healthy

        # schedule the reporting of the execution of this task
        self.dispatcher.whenWriteReady(
            channel=channel,
            call=functools.partial(
                self.report, result=result, crewstatus=crewstatus, taskstatus=taskstatus
            ),
        )

        # and go back to waiting for more
        return True

    def engage(self, task, **kwds):
        """
        Carry out the task
        """
        # just do it
        return task(**kwds)

    def report(self, channel, crewstatus, taskstatus, result, **kwds):
        """
        Post the task completion {report}
        """
        # make a report
        report = (crewstatus, taskstatus, result)
        # tell me
        self.debug.log(f"{self.pid}: sending report {report}")
        # serialize and send
        self.marshaler.send(channel=channel, item=report)
        # all done; don't reschedule
        return False

    def resign(self):
        # record my finish time; don't mess with the timer too much as it might not belong to me
        self.finish = self.timer.read()
        # close my communication channel
        self.channel.close()
        # all done
        return self

    # meta-methods
    def __init__(self, pid, channel, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my crew is; this is an opaque type, assigned to me by my recruiter
        self.pid = pid
        # save the communication channel to my twin
        self.channel = channel
        # my twin is working on nothing yet; this names the task a deadline is measured
        # against, so a report that beats its deadline can retire it
        self.task = None
        # all done
        return


# end of file
