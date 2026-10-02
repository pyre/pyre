#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a member recruited through the forkserver is a copy of the application as it
started, not of the process that asked for it: after a thread of the application takes a lock
and keeps it, a member forked from the application would wait forever for that lock, since the
thread that holds it does not exist on its side of the fork, but a member forked by the helper
finds it free
"""

# externals
import os
import threading

# support
import pyre
import journal

# the unit of time
from pyre.units.SI import second

# the lock a thread of the application takes and keeps, once the application is running
lock = threading.Lock()


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


# a task that needs the lock
class Grab(pyre.nexus.task):
    """
    A task that takes the lock, lets it go, and says so
    """

    # interface
    def execute(self, **kwds):
        """
        The body of the functor
        """
        # take the lock and let it go; in a copy of a process whose thread holds it, this waits
        # forever
        with lock:
            # nothing to do while holding it
            pass
        # say so
        journal.info("test.forkserver.poison").log("grabbed")
        # and report where i ran
        return os.getpid()


def gone(pid):
    """
    Check whether the process {pid} is gone
    """
    # carefully
    try:
        # probe it
        os.kill(pid, 0)
    # if there is no such process
    except ProcessLookupError:
        # it is gone
        return True
    # otherwise, it is still around
    return False


# the application
class Poison(pyre.application, family="tests.pyre.nexus.forkserver.poison"):
    """
    An application that poisons its own process before it asks for a crew member
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

        # the moment the lock is taken
        taken = threading.Event()

        # a thread that takes the lock and never lets it go
        def hold():
            """
            Take the lock and keep it
            """
            # take it
            lock.acquire()
            # say so
            taken.set()
            # and wait forever
            threading.Event().wait()

        # start the thread; it does not keep the process alive
        threading.Thread(target=hold, daemon=True).start()
        # wait until it has the lock
        taken.wait()

        # build a staff of one that recruits through the forkserver
        staff = pyre.nexus.staff()(name="test.forkserver.poison")
        staff.size = 1
        staff.recruiter = pyre.nexus.forkserver()
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

        # the alarm that ends the wait if the member never answers
        def expire(timestamp):
            """
            Stop the event loop
            """
            # stop
            staff.dispatcher.stop()
            # and do not reschedule
            return None

        # ask for the lock
        staff.assign(task=Grab(), callback=deliver)
        # give the member plenty of time
        staff.dispatcher.alarm(interval=60 * second, call=expire)
        # and wait
        staff.dispatcher.watch()

        # the member answered
        assert len(outcomes) == 1, outcomes
        # without an error
        pid, error = outcomes[0]
        assert error is None, error
        # from a process of its own
        assert pid != os.getpid()
        # that is not my child, since the helper forked it
        try:
            # so there is nothing to wait for
            os.waitpid(pid, os.WNOHANG)
        # which is how it should be
        except ChildProcessError:
            # good
            pass
        # otherwise
        else:
            # it is my child after all
            assert False, f"member {pid} is a child of the team's process"
        # what it said reached me
        heard = [
            page
            for _, page, notes in capture.calls
            if notes.get("channel") == "test.forkserver.poison"
        ]
        assert heard == [["grabbed"]], heard

        # send everybody home
        staff.disband()
        # the member is gone
        assert gone(pid)
        # and so is the helper, once asked to leave
        pyre.nexus.forkserver().stop()

        # all done
        return 0


# main
if __name__ == "__main__":
    # instantiate
    app = Poison(name="forkserver_poison")
    # invoke
    status = app.run()
    # and share the status with the shell
    raise SystemExit(status)


# end of file
