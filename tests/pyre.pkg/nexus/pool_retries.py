#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the stock pool
from pyre.nexus.Pool import Pool


# a task that never succeeds
class Failing(pyre.nexus.task):
    """
    A task that fails with a recoverable error every time it runs
    """

    # interface
    def execute(self):
        """
        The body of the task
        """
        # always fail, in a way that is worth trying again
        raise self.RecoverableError(description="not yet")


# a task that succeeds
class Fine(pyre.nexus.task):
    """
    A task with a recognizable result
    """

    # interface
    def execute(self):
        """
        The body of the task
        """
        # hand back a marker
        return "done"


# a pool that keeps track of what happened to its tasks
class Ledger(Pool, family="test.nexus.ledgers.ledger"):
    """
    A pool that records the outcomes it is told about
    """

    # outcome hooks
    def collect(self, task, result):
        """
        Record the {result} of {task}
        """
        # file it
        self.outcomes.append(("collect", task, result))
        # and chain up
        return super().collect(task=task, result=result)

    def requeue(self, task, error):
        """
        Record the recoverable {error} of {task}
        """
        # file it
        self.outcomes.append(("requeue", task, error))
        # and chain up, which decides whether the task is tried again
        return super().requeue(task=task, error=error)

    def abandon(self, task, error):
        """
        Record that {task} was given up on after {error}
        """
        # file it
        self.outcomes.append(("abandon", task, error))
        # and chain up
        return super().abandon(task=task, error=error)

    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # nothing has happened yet
        self.outcomes = []
        # all done
        return


def test():
    """
    Verify that a pool tries a task that keeps failing with recoverable errors only as many times
    as its {retries} allow, then abandons it with its last error, and that its batch completes
    """
    # a pool tries a failing task again three times, unless told otherwise
    assert Pool(name="test.pool.retries.default").retries == 3

    # make a pool with a single member, so the tasks run one at a time
    team = Ledger(name="test.pool.retries")
    team.size = 1
    # that tries a failing task again twice
    team.retries = 2

    # a task that never succeeds
    failing = Failing()
    # and one that does
    fine = Fine()
    # make them the workplan
    team.assemble(workplan={failing, fine})
    # and run it; the team retires when the workplan drains
    team.run()

    # the outcomes of the failing task
    failures = [(kind, error) for kind, task, error in team.outcomes if task is failing]
    # it failed three times: once, and once more for each of its two retries
    assert [kind for kind, _ in failures] == ["requeue", "requeue", "requeue", "abandon"]
    # and it was abandoned with the error of its last attempt
    _, error = failures[-1]
    # which is the recoverable error it raised
    assert isinstance(error, Failing.RecoverableError), error
    # and not one the pool made up
    assert error.description == "not yet", error.description

    # the other task
    others = [(kind, result) for kind, task, result in team.outcomes if task is fine]
    # completed, once
    assert others == [("collect", "done")], others

    # the batch completed: nothing is left to do
    assert len(team.workplan) == 0
    # nobody is left on the rosters
    assert list(team.crews()) == []
    # and no failure counts are left behind
    assert team.failures == {}

    # all done
    return team


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
