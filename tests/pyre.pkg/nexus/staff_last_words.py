#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that what a crew member says just before it dies reaches the team, and that a firewall
breach in a member is heard as well as reported
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


# a task that dies abruptly
class Boom(pyre.nexus.task):
    """
    A task that leaves a note and then takes down its crew member, report unsent
    """

    # interface
    def execute(self, **kwds):
        """
        The body of the functor
        """
        # the last words
        journal.warning("test.staff.lastwords").log("going down")
        # die without a trace
        os._exit(1)


# a task that trips a firewall
class Breach(pyre.nexus.task):
    """
    A task that breaches a firewall
    """

    # interface
    def execute(self, **kwds):
        """
        The body of the functor
        """
        # fire
        journal.firewall("test.staff.lastwords").log("impossible")
        # unreachable
        return "survived"


def test():
    # install a capturing device before anybody is forked
    capture = Capture()
    journal.chronicler.device = capture

    # build a staff of one
    staff = pyre.nexus.staff()(name="test.staff.lastwords")
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

    # assign the lethal task and spin until the outcome is delivered
    staff.assign(task=Boom(), callback=deliver)
    staff.dispatcher.watch()
    # the failure was reported as a casualty
    assert isinstance(outcomes[0][1], pyre.nexus.exceptions.Casualty)
    # the last words arrived
    words = [call for call in capture.calls if call[2].get("channel") == "test.staff.lastwords"]
    assert len(words) == 1
    sink, page, notes = words[0]
    assert sink == "alert"
    assert page == ["going down"]
    assert notes["severity"] == "warning"
    # from somebody other than me
    assert notes["pid"] != str(os.getpid())

    # assign the breaching task to the replacement and spin until the outcome is delivered
    staff.assign(task=Breach(), callback=deliver)
    staff.dispatcher.watch()
    # the failure was reported
    assert outcomes[1][0] is None
    assert outcomes[1][1] is not None
    # and the breach was heard
    words = [call for call in capture.calls if call[2].get("channel") == "test.staff.lastwords"]
    assert len(words) == 2
    sink, page, notes = words[1]
    assert sink == "memo"
    assert page == ["impossible"]
    assert notes["severity"] == "firewall"
    assert notes["pid"] != str(os.getpid())

    # send everybody home
    staff.disband()

    # all done
    return staff


# main
if __name__ == "__main__":
    test()


# end of file
