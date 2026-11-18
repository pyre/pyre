#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Exercise the pipe transport: build a pair, exchange a message, wrap raw descriptors
    """
    # externals
    import os

    # get the package
    import pyre.ipc

    # instantiate the transport
    transport = pyre.ipc.newPipe()
    # build a pair of connected channels
    parent, child = transport.open()
    # push a message through, parent to child
    parent.write(bytes=b"ping")
    # and it arrives
    assert child.read(minlen=4) == b"ping"
    # and back
    child.write(bytes=b"pong")
    # and it arrives
    assert parent.read(minlen=4) == b"pong"

    # make a raw pipe
    infd, outfd = os.pipe()
    # dress its descriptors as a channel that talks to itself
    loop = transport.wrap(infd=infd, outfd=outfd)
    # push a message through it
    loop.write(bytes=b"loop")
    # and it comes back
    assert loop.read(minlen=4) == b"loop"

    # all done
    return transport


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
