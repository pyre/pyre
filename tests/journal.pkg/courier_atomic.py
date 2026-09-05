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
    # every attempt was stamped, and cost exactly one sequence number, whether or not the
    # report of the drops was attempted along the way
    assert courier.seq == attempts
    # some were lost
    assert courier.dropped > 0
    # and the books balance
    assert courier.shipped + courier.dropped == attempts
    # the lost ones count what was owed
    owed = courier.dropped

    # drain the socket; the read end must not block either
    reader.setblocking(False)
    # collect what made it through, one record per datagram
    received = []
    # read until there is nothing left
    while True:
        # attempt to
        try:
            # read a datagram
            received.append(reader.recv(64 * 1024))
        # if the socket is empty
        except BlockingIOError:
            # done
            break

    # log once more; the far end has caught up, so this one goes out, preceded by the report
    channel.log("after")
    # the drops were reported
    assert courier.dropped == 0
    # the report and the entry cost one sequence number each
    assert courier.seq == attempts + 2
    # read the rest
    while True:
        # attempt to
        try:
            # read a datagram
            received.append(reader.recv(64 * 1024))
        # if the socket is empty
        except BlockingIOError:
            # done
            break

    # decode
    records = [journal.record.decode(line) for line in received]
    # the last two are the report and the entry that prompted it
    notice, after = records[-2:]
    # the report is on the courier's own channel, with the count in its notes
    assert notice.channel == "journal.courier"
    assert int(notice.notes["dropped"]) == owed
    # and the entry that prompted it follows
    assert after.page == ["after"]
    # the sequence numbers of the records that arrived are increasing
    sequence = [int(record.notes["seq"]) for record in records]
    assert sequence == sorted(sequence)
    assert len(set(sequence)) == len(sequence)
    # the report and the entry took the last two
    assert sequence[-2:] == [attempts + 1, attempts + 2]
    # and the gaps account for exactly the records owed
    assert sequence[-1] - len(records) == owed

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
