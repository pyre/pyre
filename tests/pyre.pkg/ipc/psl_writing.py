#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a selector says a channel is being written while a write handler waits on it or
runs, and not once the handler declines to be rescheduled
"""


def test():
    # access the package
    import pyre.ipc

    # make a selector
    s = pyre.ipc.newPSL()
    # a socket pair
    sock = pyre.ipc.newSocket().open()
    # what the handler saw
    seen = []

    # a handler that records what the selector says about its channel while it runs
    def handler(channel, **kwds):
        # record whether the channel is being written, and read
        seen.append((s.writing(channel=channel), s.reading(channel=channel)))
        # and decline to be rescheduled
        return False

    # before anybody registers, nobody writes to the channel
    assert not s.writing(channel=sock.child)
    # register write interest on the child end, which is ready to be written right away
    s.whenWriteReady(channel=sock.child, call=handler)
    # the waiting handler writes to it
    assert s.writing(channel=sock.child)
    # but nobody reads from it
    assert not s.reading(channel=sock.child)
    # spin until nothing is left to watch
    s.watch()
    # the handler ran once, writing to its channel and not reading from it
    assert seen == [(True, False)]
    # and once it declined, nobody writes to the channel
    assert not s.writing(channel=sock.child)
    # all done
    return s


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
