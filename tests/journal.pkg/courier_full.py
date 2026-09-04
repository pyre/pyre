#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    A far end that does not keep up costs records, never time; the loss is counted and reported
    """
    # externals
    import os

    # access
    import journal

    # make a pipe; nobody reads it for a while
    reader, writer = os.pipe()
    # make a courier on its write end and install it
    courier = journal.courier(descriptor=writer)
    journal.chronicler.device = courier
    # the channel
    channel = journal.info("test.courier.full")

    # a line long enough to fill any pipe buffer in a few hundred entries
    filler = "x" * 1024
    # the number of entries to attempt
    attempts = 1024
    # log them all without reading; each call must return, whatever the state of the pipe
    for _ in range(attempts):
        # log
        channel.log(filler)
    # every attempt was stamped
    assert courier.seq == attempts
    # some were lost
    assert courier.dropped > 0
    # and the books balance
    assert courier.shipped + courier.dropped == attempts
    # the lost ones count what was owed
    owed = courier.dropped

    # drain the pipe; the read end must not block either
    os.set_blocking(reader, False)
    # collect what made it through
    received = b""
    # read until there is nothing left
    while True:
        # attempt to
        try:
            # read a chunk
            chunk = os.read(reader, 64 * 1024)
        # if the pipe is empty
        except BlockingIOError:
            # done
            break
        # if the pipe is empty
        if not chunk:
            # done
            break
        # accumulate
        received += chunk

    # log once more; the far end has caught up, so this one goes out, preceded by the report
    channel.log("after")
    # the drops were reported
    assert courier.dropped == 0
    # read the rest
    while True:
        # attempt to
        try:
            # read a chunk
            chunk = os.read(reader, 64 * 1024)
        # if the pipe is empty
        except BlockingIOError:
            # done
            break
        # if the pipe is empty
        if not chunk:
            # done
            break
        # accumulate
        received += chunk

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
    assert notice.sink == "alert"
    # it carries the count in its notes
    assert int(notice.notes["dropped"]) == owed
    # and the entry that prompted it follows
    assert after.page == ["after"]
    # the sequence numbers of the records that arrived, in order, with gaps for the losses
    sequence = [record.seq for record in records]
    assert sequence == sorted(sequence)
    assert len(set(sequence)) == len(sequence)
    # the gaps account for exactly the records owed
    assert after.seq - len(records) == owed

    # clean up
    courier.close()
    os.close(reader)

    # all done
    return


# main
if __name__ == "__main__":
    # tell journal to stay away from the bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
