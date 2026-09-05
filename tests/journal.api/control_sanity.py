#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    A control survives the trip to its wire form and back, and applies to the channel it names
    """
    # access
    import journal

    # the channel
    name = "test.control"
    # a debug channel is off and non-fatal by default
    assert not journal.debug(name).active
    assert not journal.debug(name).fatal

    # a control that turns it on, saying nothing about the other flag
    control = journal.control(severity="debug", name=name, active=True)
    # its wire object carries only what was given
    assert control.raw() == {
        "journal": 1,
        "kind": "control",
        "severity": "debug",
        "name": name,
        "active": True,
    }
    # its wire form is a single line
    line = control.encode()
    assert line.endswith(b"\n")
    assert line.count(b"\n") == 1

    # the round trip
    clone = journal.control.decode(line)
    assert clone.severity == "debug"
    assert clone.name == name
    assert clone.active is True
    assert clone.fatal is None

    # applying it flips the flag it names, and only that one
    channel = clone.apply()
    assert channel.active
    assert not channel.fatal
    assert journal.debug(name).active

    # a control with both flags
    journal.control(severity="debug", name=name, active=False, fatal=True).apply()
    assert not journal.debug(name).active
    assert journal.debug(name).fatal

    # the exception decoding raises
    RecordError = journal.exceptions.RecordError

    # a helper that expects a line to be refused
    def refuse(line):
        # attempt to
        try:
            # decode
            journal.control.decode(line)
        # if it was refused
        except RecordError:
            # all good
            return
        # otherwise
        assert False, f"accepted: {line!r}"

    # a record is not a control
    record = journal.record(sink="alert", page=[], notes={}, seq=1, pid=1, time=0.0)
    refuse(record.encode())
    # nor is garbage
    refuse(b"garbage\n")
    # nor a control with a flag that is not a boolean
    refuse(b'{"journal":1,"kind":"control","severity":"debug","name":"x","active":"yes"}\n')
    # nor one without a channel
    refuse(b'{"journal":1,"kind":"control","severity":"debug"}\n')

    # a control for a severity nobody knows cannot be applied
    try:
        # attempt to
        journal.control(severity="gossip", name=name, active=True).apply()
    # it must be refused
    except RecordError:
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
