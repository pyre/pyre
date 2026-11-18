#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a team member whose report arrives without the descriptors it carried stays at
work, and that its task counts as a recoverable failure, which a pool puts back in its workplan
"""

# externals
import errno
import os
import resource

# support
import pyre

# the channel that travels
from pyre.ipc.File import File

# the stock pool
from pyre.nexus.Pool import Pool


def fill():
    """
    Lower the limit on the number of open descriptors and open as many as it allows
    """
    # get the current limits
    limits = resource.getrlimit(resource.RLIMIT_NOFILE)
    # lower the soft one, so the table is quick to fill
    resource.setrlimit(resource.RLIMIT_NOFILE, (64, limits[1]))
    # the descriptors that fill the table
    fillers = []
    # until there is no more room
    while True:
        # carefully
        try:
            # open one more
            fillers.append(os.open(os.devnull, os.O_RDONLY))
        # when the table is full
        except OSError as error:
            # make sure that is what happened
            assert error.errno == errno.EMFILE, error
            # and stop
            break
    # hand off what must be undone
    return limits, fillers


def empty(limits, fillers):
    """
    Close the {fillers} and restore the {limits}
    """
    # close the fillers
    for descriptor in fillers:
        # one at a time
        os.close(descriptor)
    # and restore the limits
    resource.setrlimit(resource.RLIMIT_NOFILE, limits)
    # all done
    return


def test():
    # make a pool
    team = Pool(name="test.pool.arrival")
    # make the channel between the team and its member
    parent, child = pyre.ipc.newSocket().open()
    # build the worker side member; nothing gets reaped here, so my own pid will do
    worker = pyre.nexus.crew(pid=os.getpid(), channel=child)
    # and the team side one
    crew = pyre.nexus.crew(pid=os.getpid(), channel=parent)
    # wired the way the recruiter does
    crew.dispatcher = team.dispatcher
    crew.marshaler = team.marshaler
    # the member is at work
    team.active.add(crew)
    # on a task
    task = pyre.nexus.task()

    # the worker finishes the task, with a file as its result
    worker.report(
        channel=child,
        crewstatus=worker.crewcodes.healthy,
        taskstatus=worker.taskcodes.completed,
        result=File.temporary(),
    )

    # fill the descriptor table
    limits, fillers = fill()
    # carefully, so the table is emptied no matter what
    try:
        # the team assesses the report
        keep = crew.assess(channel=parent, team=team, task=task)
    # whatever happened
    finally:
        # make room again
        empty(limits=limits, fillers=fillers)

    # the handler is done
    assert keep is False
    # the task is back in the workplan
    assert task in team.workplan
    # after its first recoverable failure
    assert team.failures[task] == 1
    # the member is still at work
    assert crew in team.active
    # and nothing is left waiting to be claimed
    assert parent.arrivals == []

    # clean up
    parent.close()
    # both ends
    child.close()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
