#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a team can turn a channel on or off in a running crew member, and that what the
member says afterwards reflects the change
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


# the channel under control
name = "test.staff.instruct"


# a task that whispers
class Whisper(pyre.nexus.task):
    """
    A task that says something on a debug channel, which is off unless somebody turned it on
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
        # whisper
        journal.debug(name).log(f"whisper {self.tag}")
        # and report the state of the channel where i ran
        return journal.debug(name).active


def test():
    # install a capturing device before anybody is forked
    capture = Capture()
    journal.chronicler.device = capture
    # the channel is off here
    assert not journal.debug(name).active

    # build a staff of one, so the same member serves every task
    staff = pyre.nexus.staff()(name="test.staff.instruct")
    staff.size = 1
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

    # what the member has said on the channel so far
    def heard():
        """
        The whispers that reached me
        """
        # the pages of the entries from the channel
        return [page for _, page, notes in capture.calls if notes.get("channel") == name]

    # a first task; the channel is off in the member, so nothing is heard
    staff.assign(task=Whisper(tag=1), callback=deliver)
    staff.dispatcher.watch()
    assert outcomes[0] == (False, None)
    assert heard() == []
    # the member that served it; the loop stopped before it was parked, so look at every roster
    (veteran,) = set(staff.crews())

    # turn the channel on, here and in the member
    staff.instruct(control=journal.control(severity="debug", name=name, active=True))
    # it is on here
    assert journal.debug(name).active
    # the next task, served by the same member, finds it on and its whisper is heard
    staff.assign(task=Whisper(tag=2), callback=deliver)
    staff.dispatcher.watch()
    assert outcomes[1] == (True, None)
    assert heard() == [["whisper 2"]]
    assert set(staff.crews()) == {veteran}

    # turn it off again
    staff.instruct(control=journal.control(severity="debug", name=name, active=False))
    assert not journal.debug(name).active
    # and the member falls silent
    staff.assign(task=Whisper(tag=3), callback=deliver)
    staff.dispatcher.watch()
    assert outcomes[2] == (False, None)
    assert heard() == [["whisper 2"]]

    # send everybody home
    staff.disband()

    # all done
    return staff


# main
if __name__ == "__main__":
    test()


# end of file
