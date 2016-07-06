#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#

# externals
import random, time
# support
import pyre

# my task
class Task(pyre.nexus.task):
    """
    A simple task
    """

    # interface
    def execute(self):
        """
        The body of the task
        """
        # grab a random number in the range (0,1]
        p = random.random()
        # sometimes
        if p < .1:
            # i experience a temporary failure
            raise self.RecoverableError("a temporary error")
        # sometimes
        if p < .2:
            # i fail
            raise Exception("a nasty error")
        # the rest of the time, go to sleep for a bit
        time.sleep(3*p)
        # and return
        return p


# my team manager
from pyre.nexus.Pool import Pool as pool
class Pool(pool, family='samples.teams.pool'):
    """
    Subclass to augment the behavior of the stock team manager
    """

    def welcome(self, member):
        """
        The recruiter has identified a new team member
        """
        # seed the random number generator differently on different team members
        random.seed(member.pid)
        # all done
        return self


# the application
class Application(pyre.application, family="samples.applications.pool"):
    """
    An application that employs a team to accomplish a workplan concurrently
    """

    # user configurable state
    #team = pyre.nexus.team(default=Pool)
    team = pyre.nexus.team(default=Pool)
    team.doc = "my team manager"

    tasks = pyre.properties.int(default=1)
    tasks.doc = "the number of tasks in my workplan"


    # protocol obligations
    @pyre.export
    def main(self, *args, **kwds):
        """
        The main entry point
        """
        # grab a channel
        channel = self.debug
        # show me
        channel.line()
        channel.line("  app: {app}".format(app=self))
        channel.line("    tasks: {app.tasks}".format(app=self))
        channel.line("    team: {app.team}".format(app=self))
        channel.line("      size: {app.team.size}".format(app=self))
        # flush
        channel.log()

        # make a workplan
        workplan = { Task() for _ in range(self.tasks) }
        # set it up for execution
        self.team.execute(workplan=workplan)
        # and enter the event loop
        self.team.serve()
        # all done
        return 0


# main
if __name__ == "__main__":
    # instantiate
    app = Application(name="pool")
    # run
    status = app.run()
    # share
    raise SystemExit(status)


# end of file
