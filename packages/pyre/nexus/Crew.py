# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import functools
import os
import signal
import sys
import traceback

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
        # if my twin's journal is routed to me
        if self.journal is not None:
            # listen for it, for as long as my twin lives
            self.dispatcher.whenReadReady(
                channel=self.journal, call=functools.partial(self.overhear, team=team)
            )
        # all done
        return self

    def overhear(self, channel, team):
        """
        My twin has something to say; collect the records and hand them to the team

        N.B.: this is an event handler; careful with its return value
        """
        # check it's me we are talking about
        assert channel is self.journal
        # the wire form of an entry, and the complaint about one that is not; imported here
        # because the journal package boots the framework, which imports me
        from journal import record as Record
        from journal.exceptions import RecordError

        # carefully, since my twin may be gone
        try:
            # pull whatever is there
            data = channel.read(minlen=0, maxlen=64 * 1024)
        # if the channel is broken
        except OSError:
            # my twin is gone
            data = b""
        # if there is nothing, my twin has closed its end, which only happens when it exits
        if not data:
            # if any of what it said could not be understood
            if self.garbled:
                # leave a note
                self.warning.log(f"{self.pid}: {self.garbled} garbled journal records")
            # carefully
            try:
                # release my end
                channel.close()
            # tolerating one that is already gone
            except OSError:
                # nothing further
                pass
            # and stop listening
            return False
        # add what arrived to what was left over from last time
        self.tail += data
        # split off the complete lines; the last piece is the start of a line still in transit
        *lines, self.tail = self.tail.split(b"\n")
        # go through the complete lines
        for line in lines:
            # carefully
            try:
                # decode the record
                record = Record.decode(line)
            # if it is not one
            except RecordError as error:
                # count it
                self.garbled += 1
                # leave a note
                self.debug.log(f"{self.pid}: garbled journal record: {error.reason}")
                # and move on
                continue
            # hand it to the team
            team.overhear(crew=self, record=record)
        # keep listening
        return True

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
        # so deliver the bad news
        team.abandon(
            task=task,
            error=self.RecoverableError(description=f"crew {self.pid} took too long"),
        )
        # my twin is still running, and it is exactly the kind of process that may never
        # stop. a burial gives a member that is on its way out a grace period before it
        # insists, and this one has had all the time it is going to get, so end it now
        try:
            # with prejudice; a member that has blown its deadline gets no chance to object
            os.kill(self.pid, signal.SIGKILL)
        # tolerating one that has already gone on its own
        except (OSError, ProcessLookupError):
            # nothing further
            pass
        # and now clean up after it: the burial takes it off the rosters, closes the channel,
        # hands the process to the recruiter to collect, and lets the team recruit a
        # replacement
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
        # if anybody is listening
        if self.debug.active:
            # let them know what happened
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

    def instruct(self, control):
        """
        Send my twin the {control} instruction over its journal channel
        """
        # if there is no such channel
        if self.journal is None:
            # there is nothing to do
            return self
        # send it
        self.journal.write(control.encode())
        # all done
        return self

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
        # if my journal is routed to the team
        if self.journal is not None:
            # the team may send instructions back over the same channel, and they are also
            # collected right before each task, so the channel must not block
            self.journal.setBlocking(False)
            # listen for them
            self.dispatcher.whenReadReady(channel=self.journal, call=self.obey)
        # all done
        return self

    @classmethod
    def route(cls, channel):
        """
        Send everything this process says to the journal down {channel}, for the team to hear,
        and hand back the device that ships it, which must be kept alive; a member whose journal
        is not routed has no {channel}, and keeps the device it has

        This needs nothing but the channel, so a member can route its journal before anything
        else happens, even before its own class is loaded
        """
        # if the journal is not routed
        if channel is None:
            # there is nothing to do
            return None
        # get the journal
        import journal

        # get the device that ships journal entries down a channel
        from ..ipc.Courier import Courier

        # make one for this channel; the terminal is left to the team, which replays every entry
        # it hears
        courier = Courier(channel=channel)
        # install it
        journal.chronicler.device = courier
        # and hand it off
        return courier

    def work(self):
        """
        Carry out tasks until there is nothing more to do, then end my process; this does not
        return
        """
        # assume the worst, so that anything that goes wrong is reported as a failure
        status = 1
        # and keep track of whether i got to finish; asking the interpreter whether an
        # exception is in flight does not work here: a replacement member is forked from within
        # the handler of the failure of the one it replaces, so it inherits an exception that
        # is the team's business, not mine
        crashed = True
        # carefully, since an interrupt may have landed before it was set aside
        try:
            # spin up and carry out tasks until there is nothing more to do
            status = self.run()
            # i ran my course
            crashed = False
        # if it did
        except KeyboardInterrupt:
            # leave quietly; the team reports the interruption
            status = 1
            # and this is not a crash
            crashed = False
        # a request to exit
        except SystemExit as request:
            # carries the status it asks for
            status = request.code
            # and is not a crash either
            crashed = False
        # whatever happened, my process must terminate, and it must do so here
        finally:
            # so leave; this does not return
            self.leave(status=status, crashed=crashed)

    def leave(self, status, crashed=False):
        """
        End my process with the given exit {status}; {crashed} says that i am on my way out
        because of an exception nobody handled

        A crew member is a fork of another process, so the exit handlers it would run on the way
        out belong to that process: registered by libraries in a process that had state i do not
        share, e.g. threads, which do not survive a fork. Such a handler may wait forever for
        something that exists only on the other side of the fork, and then i never leave. So i
        end my process directly, after putting my own affairs in order, and the inherited
        handlers never run
        """
        # if i got here because something went wrong that nobody handled
        if crashed:
            # say what it was, since the interpreter will not get the chance
            traceback.print_exc()
        # carefully, since nothing must get in the way of leaving
        try:
            # put my affairs in order, e.g. close what i have open for writing
            self.retire()
        # and whatever happens
        finally:
            # go through the standard streams
            for stream in (sys.stdout, sys.stderr):
                # carefully, since they may be closed or broken
                try:
                    # deliver what is pending; nothing else will
                    stream.flush()
                # if that fails
                except (OSError, ValueError):
                    # there is nothing to be done about it
                    pass
            # normalize the status the way the interpreter does: nothing means success, a
            # number is itself, and anything else is a failure
            code = 0 if status is None else status if isinstance(status, int) else 1
            # and end the process without running the exit handlers
            os._exit(code)

    def obey(self, channel):
        """
        The team has sent instructions over my journal channel; apply them

        N.B.: this is an event handler; careful with its return value
        """
        # check it's me we are talking about
        assert channel is self.journal
        # collect and apply whatever arrived; an empty read means the team has let go of its
        # end, which only happens when it is gone
        return self.heed()

    def heed(self):
        """
        Apply the instructions the team has sent so far, if any; report whether the channel is
        still open
        """
        # the wire form of an instruction, and the complaint about one that is not; imported
        # here because the journal package boots the framework, which imports me
        from journal import control as Control
        from journal.exceptions import RecordError

        # carefully
        try:
            # pull whatever is there without waiting
            data = self.journal.read(minlen=0, maxlen=64 * 1024)
        # if nothing is there right now
        except BlockingIOError:
            # the channel is open and quiet
            return True
        # if the channel is broken
        except OSError:
            # the team is gone
            data = b""
        # if the team has let go, it is gone; wind down my event loop, so nothing else keeps
        # me alive
        if not data:
            # stop
            self.stop()
            # and stop listening
            return False
        # add what arrived to what was left over from last time
        self.orders += data
        # split off the complete lines; the last piece is the start of a line still in transit
        *lines, self.orders = self.orders.split(b"\n")
        # go through the complete lines
        for line in lines:
            # carefully
            try:
                # decode and apply the instruction
                Control.decode(line).apply()
            # if it is not one, or names a channel that does not exist
            except RecordError as error:
                # leave a note
                self.debug.log(f"{self.pid}: garbled instruction: {error.reason}")
                # and move on
                continue
        # keep listening
        return True

    def checkin(self, channel):
        """
        Send my team registration now that my communication channel is open
        """
        # check it's me we are talking about
        assert channel is self.channel
        # carefully, since the team may have let go of its end before hearing from me
        try:
            # send in a healthy status code
            self.marshaler.send(channel=channel, item=self.crewcodes.healthy)
        # if the team is unreachable
        except OSError:
            # there is nothing for me here; wind down my event loop, so no other channel keeps
            # me alive
            self.stop()
            # and stop listening
            return False
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
        # if anybody is listening
        if self.debug.active:
            # leave them a note with the {task} details
            self.debug.log(f"{self.pid}: got {task}")
        # if it's a quit marker
        if task is None:
            # we are all done
            self.stop()
            # don't reschedule this handler
            return False
        # if the team can send me instructions
        if self.journal is not None:
            # apply the ones that arrived before this task, whatever order the loop saw them in
            self.heed()

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
        # boundary: anything else the task raises aborts it, and goes back in the report
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
        # if anybody is listening
        if self.debug.active:
            # let them know the report is ready
            self.debug.log(f"{self.pid}: sending report {report}")
        # carefully, since the team may be gone
        try:
            # serialize and send
            self.marshaler.send(channel=channel, item=report)
        # if the team is unreachable
        except OSError:
            # nobody will ever hear from me again; wind down my event loop
            self.stop()
        # all done; don't reschedule
        return False

    def retire(self):
        """
        Put my affairs in order: my process is about to end, and it will not run exit
        handlers or finalize what i still hold, so whatever must not be lost, e.g. a file
        open for writing, gets closed here. This runs on the crew side only
        """
        # i hold nothing of the sort
        return self

    def resign(self):
        # record my finish time; don't mess with the timer too much as it might not belong to me
        self.finish = self.timer.read()
        # close my communication channel
        self.channel.close()
        # all done
        return self

    # meta-methods
    def __init__(self, pid, channel, journal=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my id; this is an opaque type, assigned to me by my recruiter
        self.pid = pid
        # save the communication channel to my twin
        self.channel = channel
        # and the channel that carries my twin's journal entries, if any
        self.journal = journal
        # on the worker side, the device that ships them; held here so it outlives the fork
        self.courier = None
        # the start of a record still in transit from my twin
        self.tail = b""
        # the start of an instruction still in transit from my team
        self.orders = b""
        # the number of records from my twin that could not be understood
        self.garbled = 0
        # my twin is working on nothing yet; this names the task a deadline is measured
        # against, so a report that beats its deadline can retire it
        self.task = None
        # all done
        return


# end of file
