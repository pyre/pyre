#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a selector keeps reporting a channel while the handlers of that channel are
running: a handler that forks a worker must be able to find the connection it is serving
among the channels the worker has to release
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

    # a handler that records the channels the selector reports while it runs
    def handler(channel, **kwds):
        # drain the byte that woke it
        channel.read(maxlen=1)
        # record the watch list
        seen.append(set(s.channels()))
        # and decline to be rescheduled
        return False

    # register read interest on the child end
    s.whenReadReady(channel=sock.child, call=handler)
    # wake it
    sock.parent.write(b"x")
    # spin until nothing is left to watch
    s.watch()
    # the handler ran once
    assert len(seen) == 1
    # and found its own channel among the ones being watched
    assert sock.child in seen[0]
    # with the pile released afterwards
    assert list(s.channels()) == []
    # all done
    return s


# main
if __name__ == "__main__":
    test()


# end of file
