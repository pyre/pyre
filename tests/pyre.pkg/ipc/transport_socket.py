#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the socket transport: build a pair, exchange a message, wrap a received descriptor
"""


def test():
    # get the package
    import pyre.ipc

    # instantiate the transport
    transport = pyre.ipc.newSocket()
    # build a pair of connected channels
    parent, child = transport.open()
    # push a message through, parent to child
    parent.write(bytes=b"ping")
    assert child.read(minlen=4) == b"ping"
    # and back
    child.write(bytes=b"pong")
    assert parent.read(minlen=4) == b"pong"

    # build a second pair, standing in for a conversation whose descriptor changes hands
    other = transport.open()
    # ship one end's descriptor over the first pair
    parent.sendDescriptors(descriptors=[other.child.fileno()])
    # receive it on the far side
    _, descriptors = child.recvDescriptors(limit=1)
    # dress it as a channel
    borrowed = transport.wrap(descriptor=descriptors[0])
    # and verify it is connected to the other pair's parent end
    borrowed.write(bytes=b"knock")
    assert other.parent.read(minlen=5) == b"knock"

    # all done
    return transport


# main
if __name__ == "__main__":
    test()


# end of file
