#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a selector says a channel is being read while a read handler waits on it or runs,
and not once the handler declines to be rescheduled
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
        # drain the byte that woke it
        channel.read(maxlen=1)
        # record whether the channel is being read, and written
        seen.append((s.reading(channel=channel), s.writing(channel=channel)))
        # and decline to be rescheduled
        return False

    # before anybody registers, nobody reads from the channel
    assert not s.reading(channel=sock.child)
    # register read interest on the child end
    s.whenReadReady(channel=sock.child, call=handler)
    # the waiting handler reads from it
    assert s.reading(channel=sock.child)
    # but nobody writes to it
    assert not s.writing(channel=sock.child)
    # wake it
    sock.parent.write(b"x")
    # spin until nothing is left to watch
    s.watch()
    # the handler ran once, reading from its channel and not writing to it
    assert seen == [(True, False)]
    # and once it declined, nobody reads from the channel
    assert not s.reading(channel=sock.child)
    # all done
    return s


# main
if __name__ == "__main__":
    test()


# end of file
