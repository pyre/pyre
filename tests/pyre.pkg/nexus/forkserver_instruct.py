#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a journal control applied before a crew member exists reaches the member when it is
recruited through the forkserver: the member is a copy of the helper, not of the team's process,
so it cannot inherit the control, and the helper has to have been told
"""

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
name = "test.forkserver.instruct"


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


# the application
class Instruct(pyre.application, family="tests.pyre.nexus.forkserver.instruct"):
    """
    An application that turns a channel on before it has any crew members
    """

    # interface
    @pyre.export
    def main(self, *args, **kwds):
        """
        The main entry point
        """
        # install a capturing device
        capture = Capture()
        journal.chronicler.device = capture
        # the channel is off here
        assert not journal.debug(name).active

        # build a staff of one that recruits through the forkserver
        staff = pyre.nexus.staff()(name="test.forkserver.instruct")
        staff.size = 1
        staff.recruiter = pyre.nexus.forkserver()
        # start the helper now, so it exists before the channel is turned on
        staff.recruiter.start(dispatcher=staff.dispatcher)
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

        # turn the channel on before there is anybody to tell but the recruiter
        staff.instruct(control=journal.control(severity="debug", name=name, active=True))
        # it is on here
        assert journal.debug(name).active
        # the first task recruits the first member, which finds the channel on
        staff.assign(task=Whisper(tag=1), callback=deliver)
        staff.dispatcher.watch()
        assert outcomes[0] == (True, None), outcomes
        assert heard() == [["whisper 1"]], heard()

        # turn it off again
        staff.instruct(control=journal.control(severity="debug", name=name, active=False))
        # and the member falls silent
        staff.assign(task=Whisper(tag=2), callback=deliver)
        staff.dispatcher.watch()
        assert outcomes[1] == (False, None), outcomes
        assert heard() == [["whisper 1"]], heard()

        # send everybody home
        staff.disband()
        # including the helper
        staff.recruiter.stop()

        # all done
        return 0


# main
if __name__ == "__main__":
    # instantiate
    app = Instruct(name="forkserver_instruct")
    # invoke
    status = app.run()
    # and share the status with the shell
    raise SystemExit(status)


# end of file
