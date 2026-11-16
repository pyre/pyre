#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a selector stops saying a channel is being read as soon as the channel is
forgotten, even while one of its read handlers is still running
"""


def test():
    # access the package
    import pyre.ipc

    # make a selector
    s = pyre.ipc.newSelector()
    # a socket pair
    sock = pyre.ipc.newSocket().open()
    # what the handler saw
    seen = []

    # a handler that forgets its channel and records what the selector says about it
    def handler(channel, **kwds):
        # drain the byte that woke it
        channel.read(maxlen=1)
        # the channel is being read
        seen.append(s.reading(channel=channel))
        # until it is forgotten
        s.forget(channel=channel)
        # after which it is not, although this handler is still running
        seen.append(s.reading(channel=channel))
        # ask to be rescheduled, which the selector refuses for a forgotten channel
        return True

    # register read interest on the child end
    s.whenReadReady(channel=sock.child, call=handler)
    # wake it
    sock.parent.write(b"x")
    # spin until nothing is left to watch
    s.watch()
    # the handler saw its channel read, then not
    assert seen == [True, False]
    # and nobody reads from it afterwards
    assert not s.reading(channel=sock.child)
    # all done
    return s


# main
if __name__ == "__main__":
    test()


# end of file
