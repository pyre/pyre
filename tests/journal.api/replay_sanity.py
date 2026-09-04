#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Replaying a record delivers its entry to the device its channel resolves to, through the
    sink it names, with the origin in the notes, whatever the state of the local channel
    """
    # access
    import journal

    # a capturing device
    class Capture(journal.device):
        # start with an empty log
        def __init__(self, **kwds):
            # chain up
            super().__init__(name="capture", **kwds)
            # nothing recorded yet
            self.calls = []

        # record which sink each entry reached, and what it carried
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

    # the global device
    default = Capture()
    journal.chronicler.device = default
    # a per-channel device
    special = Capture()
    journal.warning("test.replay.special").device = special

    # a record from some other process, on a debug channel that is off here
    notes = {"channel": "test.replay", "severity": "debug", "application": "elsewhere"}
    record = journal.record(sink="memo", page=["from afar"], notes=notes, seq=5, pid=99, time=12.5)
    # the local channel is inactive
    assert not journal.debug("test.replay").active
    # replay anyway
    journal.replay(record=record)
    # the entry reached the global device, through the sink the record named
    assert len(default.calls) == 1
    sink, page, delivered = default.calls[0]
    assert sink == "memo"
    assert page == ["from afar"]
    # with the notes as sent, plus the origin
    assert delivered["channel"] == "test.replay"
    assert delivered["severity"] == "debug"
    assert delivered["application"] == "elsewhere"
    assert delivered["pid"] == "99"
    assert delivered["seq"] == "5"
    assert float(delivered["time"]) == 12.5

    # a record for the channel with its own device
    notes = {"channel": "test.replay.special", "severity": "warning"}
    record = journal.record(
        sink="alert", page=["for the special device"], notes=notes, seq=6, pid=99, time=13.0
    )
    # replay
    journal.replay(record=record)
    # it went to the per-channel device
    assert len(special.calls) == 1
    assert special.calls[0][0] == "alert"
    assert special.calls[0][1] == ["for the special device"]
    # and not to the global one
    assert len(default.calls) == 1

    # a record with a severity nobody knows
    notes = {"channel": "test.replay", "severity": "gossip"}
    record = journal.record(sink="alert", page=["?"], notes=notes, seq=7, pid=99, time=14.0)
    # attempt to
    try:
        # replay
        journal.replay(record=record)
    # it must be refused
    except journal.exceptions.RecordError:
        # as expected
        pass
    # anything else is a failure
    else:
        # complain
        assert False, "an unknown severity was accepted"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
