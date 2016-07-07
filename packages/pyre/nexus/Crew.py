# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import functools
# base class
from .Peer import Peer


# declaration
class Crew(Peer, family='pyre.nexus.peers.member'):
    """
    A member of a team that is executing a work plan

    Crew members use a communication {channel} to receive tasks to execute and return
    responses. This class does not provide any mechanism for crew members to communicate with
    each other.
    """

    # types
    from .TaskStatus import TaskStatus as taskcodes
    from .CrewStatus import CrewStatus as crewcodes


    # interface -- manager side
    def execute(self, team, task):
        """
        Send my worker half the {task} to be executed
        """
        # send the task
        self.marshaler.send(channel=self.channel, item=task)
        # schedule the harvesting of the task status
        self.dispatcher.whenReadReady(
            channel = self.channel,
            call = functools.partial(self.assess, team=team, task=task))
        # all done
        return self


    def dismissed(self):
        """
        My team manager has dismissed me
        """
        # send the end-of-tasks marker
        self.marshaler.send(channel=self.channel, item=None)
        # clean up
        self.resign()
        # leave a note
        self.debug.log('{me.pid}: dismissed at {me.finish:.3f}'.format(me=self))
        # all done
        return self


    # interface -- worker side
    def join(self):
        """
        Notify the {team} that I am ready to accept tasks, carry out tasks as they become
        available, and clean up when it's all done
        """
        # sign in with the team
        self.register()
        # process task assignments
        status = self.participate()
        # when everything is done
        self.resign()
        # leave a note
        self.debug.log('{me.pid}: resigned at {me.finish:.3f}'.format(me=self))
        # all done
        return status


    # meta-methods
    def __init__(self, pid, channel, **kwds):
        # chain up
        super().__init__(**kwds)

        # save my id
        self.pid = pid
        # and my channel
        self.channel = channel

        # NYI: what statistics do i maintain
        # all done
        return


    # implementation details -- manager side
    def assess(self, channel, team, task, **kwds):
        """
        Harvest the task completion status
        """
        # grab the report
        memberstatus, taskstatus, result = self.marshaler.recv(channel=channel)
        # show me on the debug channel
        self.debug.log('{me.pid}: {member}, {task}, {result}'.format(
            me=self, member=memberstatus, task=taskstatus, result=result))

        # first, let's figure out what to do with the task; if it failed due to some temporary
        # condition
        if taskstatus is self.taskcodes.failed:
            # put the task back in the workplan
            team.workplan.add(task)

        # now, let's figure out what to do with the worker; if the process is not damaged
        if memberstatus is not self.taskcodes.damaged:
            # put the worker back in the queue
            team.activate(member=self)

        # all done
        return False


    # implementation details -- worker side
    def register(self):
        # record my start time
        self.start = self.timer.lap()
        # leave a note
        self.debug.log('{me.pid}: joined at {me.start:.3f}'.format(me=self))
        # register my task handler with my event loop manager
        self.dispatcher.whenReadReady(channel=self.channel, call=self.perform)
        # all done
        return


    def participate(self):
        """
        Wait for incoming tasks
        """
        # leave a note
        self.debug.log('{me.pid}: watching for tasks'.format(me=self))
        # enter the event loop
        return self.dispatcher.watch()


    def perform(self, channel, **kwds):
        """
        A notification has arrived that indicates there is a task waiting to be executed
        """
        # extract the task from the channel
        task = self.marshaler.recv(channel=channel)
        # leave a note
        self.debug.log('{me.pid}: got {task}'.format(me=self, task=task))
        # if it's a quit marker
        if task is None:
            # we are all done; don't reschedule this handler
            return False

        # otherwise, try to
        try:
            # execute the task and collect its result
            result = task(**kwds)
        # if the task failure is recoverable
        except task.RecoverableError:
            # prepare a report with an error code for the task
            taskstatus = self.taskcodes.failed
            # a clean bill of health for the team member
            memberstatus = self.crewcodes.healthy
            # and a null result
            result = None
        # if anything else goes wrong
        except Exception as error:
            # prepare a report with an error code for the task
            taskstatus = self.taskcodes.aborted
            # mark the team member as damaged
            memberstatus = self.crewcodes.damaged
            # and a null result
            result = None
        # if all goes well
        else:
            # indicate task success
            taskstatus = self.taskcodes.completed
            # and a healthy the team member
            memberstatus = self.crewcodes.healthy

        # schedule the reporting of the execution of this task
        self.dispatcher.whenWriteReady(
            channel = channel,
            call = functools.partial(self.report,
                                     result=result,
                                     memberstatus=memberstatus,
                                     taskstatus=taskstatus))

        # and go back to waiting for more
        return True


    def report(self, channel, memberstatus, taskstatus, result, **kwds):
        """
        Post the task completion {report}
        """
        # make a report
        report = (memberstatus, taskstatus, result)
        # tell me
        self.debug.log('{me.pid}: sending report {report}'.format(me=self, report=report))
        # serialize and send
        self.marshaler.send(channel=channel, item=report)
        # all done; don't reschedule
        return False


    def resign(self):
        # record my finish time; don't mess with the timer too much as it might not belong to me
        self.finish = self.timer.lap()
        # close my communication channel
        self.channel.close()
        # all done
        return self


    # private data
    start = None
    finish = None


# end of file
