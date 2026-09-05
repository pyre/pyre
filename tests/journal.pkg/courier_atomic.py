#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    A far end whose writes are all or nothing costs exactly one sequence number per entry

    Datagram sockets never accept part of a message, so a full one refuses every record whole,
    the way a pipe on linux refuses records smaller than its atomic write size; there is never
    a pending tail to trip over, and the report of the drops is attempted on every entry
    """
    # externals
    import os
    import socket

    # access
    import journal

    # make a datagram socket pair; nobody reads it for a while
    reader, writer = socket.socketpair(socket.AF_UNIX, socket.SOCK_DGRAM)
    # make a courier on its write end and install it
    courier = journal.courier(descriptor=writer.fileno())
    journal.chronicler.device = courier
    # the channel
    channel = journal.info("test.courier.atomic")

    # a line long enough to fill any socket buffer in a few hundred entries
    filler = "x" * 1024
    # the number of entries to attempt
    attempts = 1024
    # log them all without reading; each call must return, whatever the state of the socket
    for _ in range(attempts):
        # log
        channel.log(filler)
    # every attempt was stamped, and so was every report of drops that found room to go out
    # between refusals, so the sequence runs at least as far as the attempts
    assert courier.seq >= attempts
    # some were lost
    assert courier.dropped > 0

    # drain the socket; the read end must not block either
    reader.setblocking(False)
    # collect what made it through, one record per datagram
    received = b""
    # read until there is nothing left
    while True:
        # attempt to
        try:
            # read a datagram
            received += reader.recv(64 * 1024)
        # if the socket is empty
        except BlockingIOError:
            # done
            break

    # log once more; the far end has caught up, so this one goes out, preceded by the report
    channel.log("after")
    # the drops were reported
    assert courier.dropped == 0
    # read the rest
    while True:
        # attempt to
        try:
            # read a datagram
            received += reader.recv(64 * 1024)
        # if the socket is empty
        except BlockingIOError:
            # done
            break

    # split into records; every line is whole, since records are never torn
    lines = received.splitlines(keepends=True)
    assert all(line.endswith(b"\n") for line in lines)
    # decode
    records = [journal.record.decode(line) for line in lines]
    # the last two are the report and the entry that prompted it
    notice, after = records[-2:]
    # the report is on the courier's own channel
    assert notice.channel == "journal.courier"
    assert notice.severity == "warning"
    # and the entry that prompted it follows
    assert after.page == ["after"]
    # the sequence numbers of the records that arrived are increasing
    sequence = [int(record.notes["seq"]) for record in records]
    assert sequence == sorted(sequence)
    assert len(set(sequence)) == len(sequence)
    # the reports of drops, each accounting for at least one loss
    notices = [record for record in records if record.channel == "journal.courier"]
    assert all(int(record.notes["dropped"]) > 0 for record in notices)
    reported = sum(int(record.notes["dropped"]) for record in notices)
    # the entries that made it out are the records that are not reports
    assert courier.shipped == len(records) - len(notices)
    # every attempt, the final entry included, was either shipped or reported lost
    assert courier.shipped + reported == attempts + 1
    # and the gaps in the sequence account for exactly the losses
    assert sequence[-1] - len(records) == reported

    # clean up
    courier.close()
    reader.close()
    # the courier owns the write descriptor; the socket object must not close it again
    writer.detach()

    # all done
    return


# main
if __name__ == "__main__":
    # tell journal to stay away from the bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
