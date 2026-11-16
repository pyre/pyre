#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a channel says, without waiting, whether a read would find something: bytes that
have arrived, or the end of the stream once its peer hangs up
"""


def check(near, far):
    """
    Check what {near} reports as its peer {far} writes and hangs up
    """
    # nothing has arrived yet
    assert near.pending() is False
    # the peer writes
    far.write(bytes=b"hello")
    # so something is waiting
    assert near.pending() is True
    # read it
    assert near.read(minlen=5, maxlen=5) == b"hello"
    # and nothing is waiting any more
    assert near.pending() is False
    # the peer hangs up
    far.close()
    # so a read would find the end of the stream
    assert near.pending() is True
    # which it does
    assert near.read(minlen=0, maxlen=1) == b""
    # all done
    return


def test():
    # externals
    import os

    # access the package
    import pyre.ipc

    # over a socket pair
    parent, child = pyre.ipc.newSocket().open()
    # each end reports what the other sends
    check(near=parent, far=child)
    # release the rest
    parent.close()

    # over a pair of pipes
    parent, child = pyre.ipc.newPipe().open()
    # the same way
    check(near=parent, far=child)
    # release the rest
    parent.close()

    # a channel that only writes has nothing to read
    reader, writer = os.pipe()
    # make it
    outbound = pyre.ipc.newPipe().wrap(outfd=writer)
    # so nothing is ever waiting
    assert outbound.pending() is False
    # release it
    outbound.close()
    # and the other end of the pipe
    os.close(reader)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
