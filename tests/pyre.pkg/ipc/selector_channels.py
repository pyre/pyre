#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a selector can report the channels it is currently watching
"""


def idle(channel, **kwds):
    """A do-nothing handler"""
    # decline to be rescheduled
    return False


def test():
    # access the package
    import pyre.ipc

    # make a selector
    s = pyre.ipc.newSelector()
    # a fresh selector watches nothing
    assert list(s.channels()) == []

    # make a pipe pair, whose endpoints are raw descriptors
    pin, pout = pyre.ipc.pipe()
    # and a socket pair, whose endpoints are socket objects
    sin, sout = pyre.ipc.socketpair()

    # register read interest on one end of the pipe
    s.whenReadReady(channel=pin, call=idle)
    # and write interest on the same channel, to exercise deduplication
    s.whenWriteReady(channel=pin, call=idle)
    # register read interest on one end of the socket pair
    s.whenReadReady(channel=sout, call=idle)

    # collect the watch list
    watched = list(s.channels())
    # each channel shows up exactly once, regardless of how many interests it holds
    assert len(watched) == 2
    # and the list contains precisely the registered channels
    assert set(watched) == {pin, sout}

    # all done
    return s


# main
if __name__ == "__main__":
    test()


# end of file
