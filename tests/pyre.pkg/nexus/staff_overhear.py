#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that what crew members say to the journal reaches the team's devices, attributed to
the member that said it, whatever the state of the team's own channels
"""

# externals
import os

# support
import pyre
import journal

# the unit of time
from pyre.units.SI import second


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
    A task that says a few things to the journal and reports who said them
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
        # say something on a channel that is on by default
        channel = journal.info("test.staff.overhear")
        channel.line(f"{self.tag}: first")
        channel.log(f"{self.tag}: second", tag=str(self.tag))
        # and something on a channel that is off everywhere but here
        debug = journal.debug("test.staff.overhear.quiet")
        debug.active = True
        debug.log(f"{self.tag}: whisper")
        # hand back who spoke
        return os.getpid()


def test():
    # install a capturing device before anybody is forked
    capture = Capture()
    journal.chronicler.device = capture
    # the team's own debug channel of the same name stays off
    assert not journal.debug("test.staff.overhear.quiet").active

    # build a staff of two, so attribution is observable
    staff = pyre.nexus.staff()(name="test.staff.overhear")
    staff.size = 2
    # the outcome drop box
    outcomes = []

    # the passive delivery callback; the loop runs on so every record gets collected
    def record(result, error):
        """
        Record the outcome
        """
        # file the report
        outcomes.append((result, error))
        # all done
        return

    # the alarm that winds down the event loop
    def expire(timestamp):
        """
        Stop the event loop
        """
        # ask the dispatcher to stop
        staff.dispatcher.stop()
        # and don't reschedule
        return None

    # assign two talkative tasks and let the loop run for a while
    staff.assign(task=Speak(tag=1), callback=record)
    staff.assign(task=Speak(tag=2), callback=record)
    staff.dispatcher.alarm(interval=1 * second, call=expire)
    staff.dispatcher.watch()
    # both outcomes arrived
    assert len(outcomes) == 2
    # the speakers are workers, not me; the same member may have served both tasks
    speakers = {result for result, _ in outcomes}
    assert os.getpid() not in speakers
    # every member has a journal channel
    assert all(crew.journal is not None for crew in staff.crews())

    # the entries that came from the workers
    heard = [call for call in capture.calls if call[2].get("pid") in map(str, speakers)]
    # two per task
    assert len(heard) == 4
    # go through the tasks
    for tag in (1, 2):
        # find the alert this task produced
        (alert,) = [call for call in heard if call[2].get("tag") == str(tag)]
        # unpack it
        sink, page, notes = alert
        # it came through the right sink, with its page and notes intact
        assert sink == "alert"
        assert page == [f"{tag}: first", f"{tag}: second"]
        assert notes["channel"] == "test.staff.overhear"
        assert notes["severity"] == "info"
        assert notes["function"] == "execute"
        # the speaker is one of the workers
        pid = notes["pid"]
        assert int(pid) in speakers
        # the whisper is the next thing that speaker said
        (whisper,) = [
            call
            for call in heard
            if call[2]["pid"] == pid and int(call[2]["seq"]) == int(notes["seq"]) + 1
        ]
        # unpack it
        sink, page, notes = whisper
        # it was heard even though my own channel of that name is off
        assert sink == "memo"
        assert page == [f"{tag}: whisper"]
        assert notes["channel"] == "test.staff.overhear.quiet"
        assert notes["severity"] == "debug"
        # and it carries the time it was flushed
        assert float(notes["time"]) > 0

    # send everybody home
    staff.disband()

    # all done
    return staff


# main
if __name__ == "__main__":
    test()


# end of file
