#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


"""
Build two processes that communicate using pickler over a pair of pipes
"""


def test():
    # externals
    import os
    # access the package
    import pyre.ipc

    # make a pickler
    m = pyre.ipc.newPickler()
    # and a pair of pipes
    parent, child = pyre.ipc.pipe()

    # fork
    pid = os.fork()
    # in the parent process
    if pid > 0:
        # invoke the parent behavior
        return onParent(marshaller=m, pipe=parent)
    # in the child
    return onChild(marshaller=m, pipe=child)


# the trivial messages
hello = "hello"
goodbye = "goodbye"


def onParent(marshaller, pipe):
    """Send a simple message and wait for the response"""
    # send a message
    marshaller.send(hello, pipe)
    # get the response
    response = marshaller.recv(pipe)
    # check it
    assert response == goodbye
    # and return
    return


def onChild(marshaller, pipe):
    """Wait for a message and send a response"""
    # get the message
    message = marshaller.recv(pipe)
    # check it
    assert message == hello
    # send the response
    marshaller.send(goodbye, pipe)
    # and return
    return


# main
if __name__ == "__main__":
    test()


# end of file
