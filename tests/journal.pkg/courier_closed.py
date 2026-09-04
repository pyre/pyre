#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    A far end that goes away silences the courier without raising
    """
    # externals
    import os

    # access
    import journal

    # make a pipe
    reader, writer = os.pipe()
    # make a courier on its write end and install it
    courier = journal.courier(descriptor=writer)
    journal.chronicler.device = courier
    # the channel
    channel = journal.info("test.courier.closed")

    # with the far end present, an entry goes out
    channel.log("present")
    assert courier.shipped == 1
    assert not courier.dead

    # take the far end away
    os.close(reader)
    # logging must not raise
    channel.log("absent")
    # the courier noticed
    assert courier.dead
    # the entry was stamped but not shipped
    assert courier.seq == 2
    assert courier.shipped == 1
    # and from now on nothing is even stamped
    channel.log("silence")
    assert courier.seq == 2

    # closing a dead courier is harmless
    courier.close()
    # and so is closing it again
    courier.close()

    # all done
    return


# main
if __name__ == "__main__":
    # tell journal to stay away from the bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
