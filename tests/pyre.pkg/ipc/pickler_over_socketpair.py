#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Build two processes that communicate using pickler over a socket pair
"""


def test():
    # externals
    import os

    # access the package
    import pyre.ipc

    # make a pickler
    m = pyre.ipc.newPickler()
    # and a pair of connected channels
    parent, child = pyre.ipc.newSocket().open()

    # fork
    pid = os.fork()
    # in the parent process
    if pid > 0:
        # invoke the parent behavior
        return onParent(child_pid=pid, marshaler=m, channel=parent)
    # in the child
    return onChild(marshaler=m, channel=child)


# the trivial messages
hello = "hello"
goodbye = "goodbye"


def onParent(child_pid, marshaler, channel):
    """Send a simple message and wait for the response"""
    # externals
    import os

    # send a message
    marshaler.send(hello, channel)
    # get the response
    response = marshaler.recv(channel)
    # check it
    assert response == goodbye
    # harvest the child and verify it exited cleanly
    _, status = os.waitpid(child_pid, 0)
    assert status == 0
    # and return
    return


def onChild(marshaler, channel):
    """Wait for a message and send a response"""
    # get the message
    message = marshaler.recv(channel)
    # check it
    assert message == hello
    # send the response
    marshaler.send(goodbye, channel)
    # and return
    return


# main
if __name__ == "__main__":
    test()


# end of file
