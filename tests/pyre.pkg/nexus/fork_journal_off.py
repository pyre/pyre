#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a recruiter told not to route the journal of its crew members opens no channel
for it, and the team hears nothing
"""

# externals
import os

# support
import pyre
import journal


# a capturing device
class Capture(journal.device):
    """
    A device that remembers every entry it is handed
    """

    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(name="capture", **kwds)
        # nothing recorded yet
        self.calls = []
        # all done
        return

    # interface
    def alert(self, entry):
        # a user-facing alert
        self.calls.append(("alert", list(entry.page), dict(entry.notes)))
        # all done
        return self

    def memo(self, entry):
        # a developer-facing memo
        self.calls.append(("memo", list(entry.page), dict(entry.notes)))
        # all done
        return self

    def help(self, entry):
        # a help screen
        self.calls.append(("help", list(entry.page), dict(entry.notes)))
        # all done
        return self


# a task that talks
class Speak(pyre.nexus.task):
    """
    A task that says something to the journal and reports who said it
    """

    # interface
    def execute(self, **kwds):
        """
        The body of the functor
        """
        # say something; it goes to my inherited copy of the team's device, and no further
        journal.info("test.fork.journal.off").log("unheard")
        # hand back who spoke
        return os.getpid()


def test():
    # install a capturing device before anybody is forked
    capture = Capture()
    journal.chronicler.device = capture

    # build a staff of one
    staff = pyre.nexus.staff()(name="test.fork.journal.off")
    staff.size = 1
    # whose recruiter does not route the journal
    staff.recruiter.journal = False
    # the outcome drop box
    outcomes = []

    # the delivery callback
    def deliver(result, error):
        """
        Record the outcome and stop the event loop
        """
        # file the report
        outcomes.append((result, error))
        # and wind down
        staff.dispatcher.stop()
        # all done
        return

    # assign the task and spin until the outcome is delivered
    staff.assign(task=Speak(), callback=deliver)
    staff.dispatcher.watch()
    # the outcome arrived
    speaker, error = outcomes[0]
    assert error is None
    assert speaker != os.getpid()
    # the member has no journal channel
    assert all(crew.journal is None for crew in staff.crews())
    # and nothing it said reached me
    assert not [call for call in capture.calls if call[2].get("channel") == "test.fork.journal.off"]

    # send everybody home
    staff.disband()

    # all done
    return staff


# main
if __name__ == "__main__":
    test()


# end of file
