#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a manifest turns channels into tokens and back: the descriptors of every channel
declared are collected in order, and each token rebuilds a channel of the same kind from the
descriptors that arrive
"""


def test():
    # externals
    import os

    # access the package
    import pyre.ipc

    # a pair of pipe channels
    pipes = pyre.ipc.newPipe().open()
    # and a pair of socket channels
    sockets = pyre.ipc.newSocket().open()

    # the manifest of the message on its way out
    outgoing = pyre.ipc.manifest()
    # declare a channel of each kind
    pipe = outgoing.declare(pipes.child)
    # one at a time
    socket = outgoing.declare(sockets.child)
    # the descriptors of both were collected, in order
    assert outgoing.descriptors == pipes.child.descriptors() + sockets.child.descriptors()
    # the pipe's take the first two places
    assert (pipe["first"], pipe["count"]) == (0, 2)
    # and the socket's the third
    assert (socket["first"], socket["count"]) == (2, 1)

    # the descriptors arrive as copies, under numbers of their own
    copies = [os.dup(descriptor) for descriptor in outgoing.descriptors]
    # into the manifest of the message on its way in
    incoming = pyre.ipc.manifest(descriptors=copies)
    # which rebuilds the pipe channel
    rebuiltPipe = incoming.claim(token=pipe)
    # and the socket channel
    rebuiltSocket = incoming.claim(token=socket)
    # each of the right kind
    assert type(rebuiltPipe) is type(pipes.child)
    # both of them
    assert type(rebuiltSocket) is type(sockets.child)
    # and made of the copies
    assert rebuiltPipe.descriptors() + rebuiltSocket.descriptors() == copies

    # the rebuilt pipe channel talks to the parent end
    rebuiltPipe.write(bytes=b"pipe")
    # which hears it
    assert pipes.parent.read(minlen=4, maxlen=4) == b"pipe"
    # and so does the rebuilt socket channel
    rebuiltSocket.write(bytes=b"socket")
    # whose parent end hears it
    assert sockets.parent.read(minlen=6, maxlen=6) == b"socket"

    # clean up
    for channel in (*pipes, *sockets, rebuiltPipe, rebuiltSocket):
        # one channel at a time
        channel.close()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
