#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the pickler reports a dead peer with {EndOfStream}, and that message framing
survives fragmented and back-to-back arrivals
"""

# externals
import os
import struct
import time

# access the package
import pyre.ipc

# the exception under test
from pyre.ipc.exceptions import EndOfStream


def test():
    # build the marshaler
    m = pyre.ipc.newPickler()

    # a channel that closes cleanly between messages: no header at all
    parent, child = pyre.ipc.newSocket().open()
    child.close()
    # attempt to
    try:
        # read from the dead channel
        m.recv(channel=parent)
        # which must not succeed
        assert False
    # the marshaler reports the end of the stream
    except EndOfStream as error:
        # with nothing received
        assert error.received == 0
        # of a header's worth expected
        assert error.expected == m.headerSize

    # a peer that dies mid-header
    parent, child = pyre.ipc.newSocket().open()
    # two bytes of a four byte header
    child.write(bytes=b"\x10\x00")
    # and gone
    child.close()
    # attempt to
    try:
        # read the truncated header
        m.recv(channel=parent)
        # which must not succeed
        assert False
    # the marshaler reports the end of the stream
    except EndOfStream as error:
        # with the fragment accounted for
        assert error.received == 2
        assert error.expected == m.headerSize

    # a peer that dies mid-body
    parent, child = pyre.ipc.newSocket().open()
    # a header that promises much more than what follows
    child.write(bytes=struct.pack(m.packing, 100) + b"stub")
    # and gone
    child.close()
    # attempt to
    try:
        # read the truncated message
        m.recv(channel=parent)
        # which must not succeed
        assert False
    # the marshaler reports the end of the stream
    except EndOfStream as error:
        # with the fragment accounted for
        assert error.received == 4
        assert error.expected == 100

    # a healthy peer whose message arrives in fragments that split the header
    parent, child = pyre.ipc.newSocket().open()
    # fork a dribbler
    pid = os.fork()
    # in the child process
    if pid == 0:
        # assemble a complete message
        import pickle

        body = pickle.dumps("dribbled")
        message = struct.pack(m.packing, len(body)) + body
        # send the first two bytes, splitting the header
        child.write(bytes=message[:2])
        # let the reader wake up on the fragment
        time.sleep(0.2)
        # send the rest
        child.write(bytes=message[2:])
        # and leave
        os._exit(0)
    # in the parent, the read blocks until the message completes
    assert m.recv(channel=parent) == "dribbled"
    # harvest the dribbler and verify it exited cleanly
    _, status = os.waitpid(pid, 0)
    assert status == 0

    # back-to-back messages must not bleed into each other: the first read takes exactly
    # its own message, even with the second already buffered
    parent, child = pyre.ipc.newSocket().open()
    m.send(item="first", channel=child)
    m.send(item="second", channel=child)
    assert m.recv(channel=parent) == "first"
    assert m.recv(channel=parent) == "second"

    # all done
    return m


# main
if __name__ == "__main__":
    test()


# end of file
