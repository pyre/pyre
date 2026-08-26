#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that revocation withdraws a subscriber: the last withdrawal drops a queued task, and
the outcome of work already in flight is quietly discarded
"""

# support
import pyre


# a task with a recognizable result
class Echo(pyre.nexus.task):
    """
    A task that reports its tag
    """

    # metamethods
    def __init__(self, tag, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my tag
        self.tag = tag
        # all done
        return

    # interface
    def execute(self, **kwds):
        """
        The body of the functor
        """
        # hand back my tag
        return self.tag


def test():
    # build a staff of one
    staff = pyre.nexus.staff()(name="test.staff.revoke")
    staff.size = 1
    # the record of deliveries
    served = []

    # the delivery callback factory
    def deliver(expected):
        """
        Build a callback that records a delivery, stopping when {expected} are in
        """

        # the callback
        def callback(result, error):
            """
            Record the outcome
            """
            # every surviving task succeeds
            assert error is None
            # record
            served.append(result)
            # once the survivors are all in
            if len(served) == expected:
                # wind down
                staff.dispatcher.stop()
            # all done
            return

        # hand it off
        return callback

    # a callback that must never fire
    def betrayed(result, error):
        """
        The callback of a revoked request
        """
        # getting here is the failure
        assert False, "a revoked callback fired"

    # queue three tasks; the middle one will be revoked before the loop runs
    a = Echo(tag="a")
    b = Echo(tag="b")
    c = Echo(tag="c")
    keeper = deliver(expected=2)
    staff.assign(task=a, callback=keeper)
    staff.assign(task=b, callback=betrayed)
    staff.assign(task=c, callback=keeper)
    # withdraw the middle request; it was queued, so the task is dropped outright
    staff.revoke(task=b, callback=betrayed)
    # the workplan shrank
    assert len(staff.workplan) == 2
    # and so did the ledger
    assert len(staff.pending) == 2

    # revoking something never assigned is a quiet no-op
    staff.revoke(task=Echo(tag="ghost"), callback=betrayed)

    # spin until the survivors are served
    staff.dispatcher.watch()
    # newest first, without the revoked task
    assert served == ["c", "a"], f"unexpected service: {served}"

    # now the in-flight story: withdraw from a task that a crew member already picked up
    d = Echo(tag="d")
    staff.assign(task=d, callback=betrayed)
    # simulate the pickup: the task leaves the queue, its ledger remains
    picked, _ = staff.workplan.popitem()
    assert picked is d
    # the requester goes away
    staff.revoke(task=d, callback=betrayed)
    # the ledger survives, empty, awaiting the in-flight outcome
    assert staff.pending[d] == []
    # the outcome arrives and is quietly discarded: no firewall, no callback
    staff.collect(task=d, result="d")
    # and the ledger is settled
    assert d not in staff.pending

    # send everybody home
    staff.disband()
    # all done
    return staff


# main
if __name__ == "__main__":
    test()


# end of file
