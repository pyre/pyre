#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that sending a message hands back its manifest, which names the channels that travelled
inside it, in the order they were met, and nothing for a message without channels
"""


def test():
    # access the package
    import pyre.ipc

    # the channel the messages travel over
    parent, child = pyre.ipc.newSocket().open()
    # and the marshaler
    pickler = pyre.ipc.newPickler()

    # a message without channels
    plain = pickler.send(item={"note": "nothing to carry"}, channel=parent)
    # names none
    assert plain.channels == []

    # a pair of pipe channels
    pipes = pyre.ipc.newPipe().open()
    # and a pair of socket channels
    sockets = pyre.ipc.newSocket().open()
    # travel inside the next message
    manifest = pickler.send(item=[pipes.child, sockets.child], channel=parent)
    # whose manifest names them, in order
    assert manifest.channels == [pipes.child, sockets.child]
    # along with their descriptors
    assert manifest.descriptors == pipes.child.descriptors() + sockets.child.descriptors()

    # both messages arrive
    assert pickler.recv(channel=child) == {"note": "nothing to carry"}
    # the second one with copies of the channels
    copies = pickler.recv(channel=child)

    # clean up
    for channel in (*pipes, *sockets, *copies, parent, child):
        # one channel at a time
        channel.close()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
