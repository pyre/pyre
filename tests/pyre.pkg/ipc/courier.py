#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the channel courier ships journal entries down a channel, through a copy of its
writable end that outlives the channel itself
"""


def test():
    # support
    import journal
    import pyre

    # make a channel
    parent, child = pyre.ipc.newSocket().open()
    # make a courier for one end
    courier = pyre.ipc.courier(channel=child)
    # which writes through a descriptor of its own
    assert courier.descriptor != child.outbound
    # so the channel can be closed
    child.close()
    # remember the device in place
    previous = journal.chronicler.device
    # and install the courier, which can still ship
    journal.chronicler.device = courier
    # make a channel
    channel = journal.info("test.ipc.courier")
    # and say something
    channel.log("hello")
    # put the previous device back
    journal.chronicler.device = previous
    # read the record
    line = parent.read(minlen=1, maxlen=64 * 1024)
    # decode it
    record = journal.record.decode(line)
    # it is the entry that was logged
    assert record.page == ["hello"]
    # on the channel it was logged on
    assert record.notes["channel"] == "test.ipc.courier"
    # clean up
    courier.close()
    # both ends
    parent.close()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
