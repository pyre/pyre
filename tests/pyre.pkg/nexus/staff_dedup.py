#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that tasks that compare equal are executed once, with every requester receiving the
shared outcome
"""

# support
import pyre


# a task whose identity is its tag
class Fetch(pyre.nexus.task):
    """
    A task that stamps its result with an execution-unique marker
    """

    # metamethods
    def __init__(self, tag, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my tag
        self.tag = tag
        # all done
        return

    def __hash__(self):
        # my identity is my tag
        return hash(self.tag)

    def __eq__(self, other):
        # two fetches of the same tag are the same work
        return type(other) is type(self) and other.tag == self.tag

    # interface
    def execute(self, **kwds):
        """
        The body of the functor
        """
        # a marker minted fresh per execution
        import uuid

        # so identical results prove a shared execution
        return (self.tag, str(uuid.uuid1()))


def test():
    # build a staff of one
    staff = pyre.nexus.staff()(name="test.staff.dedup")
    staff.size = 1
    # the outcome drop box
    outcomes = []

    # the delivery callback factory
    def deliver(label):
        """
        Build a callback that records under {label}
        """

        # the callback
        def callback(result, error):
            """
            Record the outcome, and stop once both subscribers are served
            """
            # every task succeeds
            assert error is None
            # record
            outcomes.append((label, result))
            # once both subscribers hear back
            if len(outcomes) == 2:
                # wind down
                staff.dispatcher.stop()
            # all done
            return

        # hand it off
        return callback

    # two equal requests from two different subscribers
    staff.assign(task=Fetch(tag="tile"), callback=deliver(label="first"))
    staff.assign(task=Fetch(tag="tile"), callback=deliver(label="second"))
    # the second joined the first: only one task is queued
    assert len(staff.workplan) == 1
    # with both subscribers on its ledger
    assert len(staff.pending) == 1

    # spin until both are served
    staff.dispatcher.watch()

    # both subscribers heard back
    assert {label for label, _ in outcomes} == {"first", "second"}
    # with the identical result, proving a single execution
    first, second = (result for _, result in outcomes)
    assert first == second

    # send everybody home
    staff.disband()
    # all done
    return staff


# main
if __name__ == "__main__":
    test()


# end of file
