#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Exercise a selector watching over file descriptors
"""

# externals
import os
import struct
import pickle
import pyre.ipc

# if necessary
import journal
parentdbg = journal.debug("selector.parent")
# parentdbg.active = True
childdbg = journal.debug("selector.child")
# childdbg.active = True

# the packing format
fmt = "<L"

def test():
    # build the communication channels
    from_child, to_parent = os.pipe()
    from_parent, to_child = os.pipe()
    
    # fork
    pid = os.fork()
    # in the parent process
    if pid > 0:
        # invoke the parent behavior
        return onParent(child_pid=pid, in_fd=from_child, out_fd=to_child)

    # in the child process
    return onChild(in_fd=from_parent, out_fd=to_parent)


def onParent(child_pid, in_fd, out_fd):
    # observe the parent selector at work
    # journal.debug("pyre.ipc.selector").active = True
    
    # write-ready handler
    def parent_send(selector, **kwds):
        """send a string to the child"""

        # register the response handler; do this early to avoid race conditions
        parentdbg.log("parent: registering the response handler")
        selector.notifyOnReadReady(fd=in_fd, handler=parent_get)

        parentdbg.log("parent: preparing the message")
        # create the payload
        message = pickle.dumps("Hello {}!".format(child_pid))
        # pack the length marker
        length = struct.pack(fmt, len(message))

        # send the message
        parentdbg.log("parent: sending the message")
        os.write(out_fd, length)
        os.write(out_fd, message)
        parentdbg.log("parent: done sending the message")

        # and return {False} so the selector stops watching the output channel
        return False

    # read-ready handler
    def parent_get(selector, **kwds):
        """receive the response from the child"""

        parentdbg.log("parent: getting response from child")
        # get the length of the message
        length, = struct.unpack(fmt, os.read(in_fd, struct.calcsize(fmt)))
        parentdbg.log("length={}".format(length))
        # get the message
        message = pickle.loads(os.read(in_fd, length))
        parentdbg.log("message={!r}".format(message))
        # check it
        parentdbg.log("parent: checking child response")
        assert message == "Goodbye from {}!".format(child_pid)
        parentdbg.log("parent: all good")
        # and return {False} so the selector stops watching the input channel
        return False

    # instantiate a selector
    parentdbg.log("parent: building a selector")
    s = pyre.ipc.selector()
    # let me know when my pipe TO the child is ready for writing
    parentdbg.log("parent: registering the child response handler")
    s.notifyOnWriteReady(fd=out_fd, handler=parent_send)
    # invoke the selector
    parentdbg.log("parent: initiating exchange")
    s.watch()
    parentdbg.log("parent: all done; exiting")
    # all done
    return


def onChild(in_fd, out_fd):

    # observe the child selector at work
    # journal.debug("pyre.ipc.selector").active = True

    # get my pid
    child_pid = os.getpid()

    # read-read handler
    def child_get(selector, **kwds):
        """receive a message from my parent"""
        childdbg.log("child: receiving message from parent")
        # get the length of the message
        length, = struct.unpack(fmt, os.read(in_fd, struct.calcsize(fmt)))
        childdbg.log("length={}".format(length))
        # get the message
        message = pickle.loads(os.read(in_fd, length))
        childdbg.log("message={!r}".format(message))
        # check it
        childdbg.log("child: checking it")
        assert message == "Hello {}!".format(child_pid)
        childdbg.log("child: all good")
        # register the response handler
        parentdbg.log("child: registering the response sender")
        selector.notifyOnWriteReady(out_fd, child_send)
        # and return {False} so the selector stops watching the input channel
        return False

    def child_send(selector, **kwds):
        """send a response to my parent"""

        childdbg.log("child: preparing the response")
        # create the payload
        message = pickle.dumps("Goodbye from {}!".format(child_pid))
        # pack the length marker
        length = struct.pack(fmt, len(message))

        # send the message
        childdbg.log("child: sending the response")
        os.write(out_fd, length)
        os.write(out_fd, message)
        childdbg.log("child: done sending the response")

        # and return {False} so the selector stops watching the output channel
        return False

    # instantiate a selector
    childdbg.log("child: building a selector")
    s = pyre.ipc.selector()
    # let me know when my pipe FROM my parent is ready for writing
    childdbg.log("child: registering the child response handler")
    s.notifyOnReadReady(fd=in_fd, handler=child_get)
    # invoke the selector
    childdbg.log("child: waiting for exchange")
    s.watch()
    childdbg.log("child: all done; exiting")

    # all done
    return
    

# main
if __name__ == "__main__":
    test()


# end of file 
