#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    A courier installed on the chronicler ships an entry as a record down its descriptor
    """
    # externals
    import os
    import socket

    # access
    import journal

    # make a pipe
    reader, writer = os.pipe()
    # make a courier on its write end
    courier = journal.courier(descriptor=writer)
    # check its name
    assert courier.name == "courier"
    # and its initial state
    assert courier.seq == 0
    assert courier.shipped == 0
    assert courier.dropped == 0
    assert not courier.dead

    # make it the default device
    journal.chronicler.device = courier
    # and check the assignment sticks
    assert journal.chronicler.device is courier

    # make a channel
    channel = journal.info("test.courier")
    # and log something
    channel.log("hello world")

    # the record made it out
    assert courier.seq == 1
    assert courier.shipped == 1
    assert courier.dropped == 0
    # read it
    line = os.read(reader, 64 * 1024)
    # exactly one line
    assert line.endswith(b"\n")
    assert line.count(b"\n") == 1
    # decode it
    record = journal.record.decode(line)
    # the sink follows from the severity
    assert record.sink == "alert"
    # the page is what was logged
    assert record.page == ["hello world"]
    # the notes carry the channel, the severity, and the location
    assert record.channel == "test.courier"
    assert record.severity == "info"
    assert record.notes["filename"].endswith("courier_sanity.py")
    assert record.notes["function"] == "test"
    assert "line" in record.notes
    # and the origin: who, when, and where
    assert record.notes["seq"] == "1"
    assert record.notes["pid"] == str(os.getpid())
    assert float(record.notes["time"]) > 0
    assert record.notes["host"] == socket.gethostname()

    # closing releases the descriptor
    courier.close()
    assert courier.dead
    # so the reader sees the end of the stream
    assert os.read(reader, 1) == b""
    # and closing again is harmless
    courier.close()

    # clean up
    os.close(reader)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
