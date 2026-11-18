#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import os
import pyre.ipc

# if necessary
import journal

# the channel that narrates the parent side of the exchange
parentdbg = journal.debug("psl.parent")
# parentdbg.active = True
# and the one for the child side
childdbg = journal.debug("psl.child")
# childdbg.active = True


def test():
    """
    Exercise a PSL selector watching over the ends of a socket pair
    """
    # build the marshaler
    m = pyre.ipc.newPickler()
    # and the communication channels
    parent, child = pyre.ipc.newSocket().open()

    # fork
    pid = os.fork()
    # in the parent process
    if pid > 0:
        # invoke the parent behavior
        return onParent(child_pid=pid, marshaler=m, channel=parent)

    # in the child process
    return onChild(marshaler=m, channel=child)


def onParent(child_pid, marshaler, channel):
    """
    Send a greeting to the child over {channel}, and check its response
    """
    # say what is happening
    parentdbg.log("parent: building a selector")
    # and instantiate a selector
    s = pyre.ipc.newPSL()

    # write-ready handler
    def parent_send(channel, **kwds):
        """
        Send a string to the child
        """
        # register the response handler; do this early to avoid race conditions
        parentdbg.log("parent: registering the response handler")
        # by asking to hear when the response arrives
        s.whenReadReady(channel=channel, call=parent_get)

        # say what is happening
        parentdbg.log("parent: preparing the message")
        # prepare the message
        message = f"Hello {child_pid}!"

        # send the message
        parentdbg.log("parent: sending the message")
        # through the marshaler
        marshaler.send(item=message, channel=channel)
        # and say so
        parentdbg.log("parent: done sending the message")

        # and return {False} so the selector stops watching the output channel
        return False

    # read-ready handler
    def parent_get(channel, **kwds):
        """
        Receive the response from the child
        """
        # say what is happening
        parentdbg.log("parent: getting response from child")
        # get the response
        message = marshaler.recv(channel)
        # show it
        parentdbg.log(f"message={message!r}")
        # check it
        parentdbg.log("parent: checking child response")
        # against what the child was asked to say
        assert message == f"Goodbye from {child_pid}!"
        # and say so
        parentdbg.log("parent: all good")
        # and return {False} so the selector stops watching the input channel
        return False

    # let me know when my channel TO the child is ready for writing
    parentdbg.log("parent: registering the child response handler")
    # by asking to hear when the channel can take the greeting
    s.whenWriteReady(channel=channel, call=parent_send)
    # invoke the selector
    parentdbg.log("parent: initiating exchange")
    # and let it run until there is nothing left to watch
    s.watch()
    # harvest the child
    _, status = os.waitpid(child_pid, 0)
    # and verify it exited cleanly
    assert status == 0
    # say so
    parentdbg.log("parent: all done; exiting")
    # all done
    return


def onChild(marshaler, channel):
    """
    Receive the greeting of the parent over {channel}, check it, and respond
    """
    # say what is happening
    childdbg.log("child: building a selector")
    # and instantiate a selector
    s = pyre.ipc.newPSL()

    # get my pid
    child_pid = os.getpid()

    # read-ready handler
    def child_get(channel, **kwds):
        """
        Receive a message from my parent
        """
        # say what is happening
        childdbg.log("child: receiving message from parent")
        # get the message
        message = marshaler.recv(channel)
        # show it
        childdbg.log(f"message={message!r}")
        # check it
        childdbg.log("child: checking it")
        # against what the parent was supposed to say
        assert message == f"Hello {child_pid}!"
        # and say so
        childdbg.log("child: all good")
        # register the response handler
        childdbg.log("child: registering the response sender")
        # by asking to hear when the channel can take the response
        s.whenWriteReady(channel=channel, call=child_send)
        # and return {False} so the selector stops watching the input channel
        return False

    # write-ready handler
    def child_send(channel, **kwds):
        """
        Send a response to my parent
        """
        # say what is happening
        childdbg.log("child: preparing the response")
        # create the payload
        message = f"Goodbye from {child_pid}!"

        # send the message
        childdbg.log("child: sending the response")
        # through the marshaler
        marshaler.send(item=message, channel=channel)
        # and say so
        childdbg.log("child: done sending the response")

        # and return {False} so the selector stops watching the output channel
        return False

    # let me know when my channel FROM my parent is ready for reading
    childdbg.log("child: registering the child response handler")
    # by asking to hear when the greeting arrives
    s.whenReadReady(channel=channel, call=child_get)
    # invoke the selector
    childdbg.log("child: waiting for exchange")
    # and let it run until there is nothing left to watch
    s.watch()
    # say so
    childdbg.log("child: all done; exiting")

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
