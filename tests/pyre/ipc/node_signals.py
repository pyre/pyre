#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Verify that the node base class handles signals properly
"""

# externals
import os
import sys
import pyre
import signal
# access the ipc package
import pyre.ipc


# the launcher
def test():
    # testing the delivery of signals is a bit tricky. {fork} is not sufficient: there must be
    # an {exec} as well, otherwise signals do get delivered properly

    # grab the configuration store
    config = pyre.executive.configurator

    # if this is the fork/exec child
    if 'child' in config:
        # spit out the command line
        # print("child:", sys.argv)
        # grab the file descriptors
        infd = int(config["infd"])
        outfd = int(config["outfd"])
        # convert them into a channel
        channel = pyre.ipc.pipe(infd=infd, outfd=outfd)
        # invoke the child behavior
        return onChild(channel=channel)

    # otherwise, set the parent/child process context
    # build the communication channels
    parent, child = pyre.ipc.pipe.open()

    # fork
    pid = os.fork()
    # in the parent process
    if pid > 0:
        # invoke the parent behavior
        return onParent(childpid=pid, channel=parent)

    # in the child process, build the new command line
    argv = [sys.executable] + sys.argv + [
        "--child",
        "--infd={}".format(child.infd),
        "--outfd={}".format(child.outfd)
        ]
    # print("execv:", argv)
    # and exec
    return os.execv(sys.executable, argv)


# the parent behavior
def onParent(childpid, channel):
    """
    The parent waits until the pipe to the child is ready for writing and then sends a SIGHUP
    to the child. The child is supposed to respond by writing 'reloaded' to the pipe, so the
    parent schedules a handler to receive the message and respond by issuing a SIGTERM, which
    kills the child. The parent harvest the exit status, checks it and terminates.
    """

    # debug
    pdbg = journal.debug("parent")
    # log
    pdbg.log("in the parent process")

    # base class
    from pyre.ipc.Node import Node
    # subclass Node
    class node(Node):

        def recvReady(self, **unused):
            # log
            pdbg.log("receiving message from child")
            # receive
            message = self.marshaller.recv(channel=self.channel)
            # log and check
            pdbg.log("child said {!r}".format(message))
            assert message == 'ready'
            # register the handler for the response to 'reload'
            self.dispatcher.notifyOnReadReady(fd=self.channel.infd, handler=self.recvReloaded)
            # issue the 'reload' signal
            os.kill(childpid, signal.SIGHUP)
            
            # don't reschedule this handler
            return False

        def recvReloaded(self, **unused):
            """check the response to 'reload' and send 'terminate'"""
            # log
            pdbg.log("receiving message from child")
            # receive
            message = self.marshaller.recv(channel)
            # check it
            pdbg.log("checking it")
            assert message == "reloaded"
            # now, send a 'terminate' to my child
            pdbg.log("sending 'terminate'")
            os.kill(childpid, signal.SIGTERM)
            # don't reschedule this handler
            pdbg.log("all good")
            return False

        def __init__(self, channel, **kwds):
            super().__init__(**kwds)
            self.channel = channel
            
            pdbg.log("registering 'recvReady'")
            self.dispatcher.notifyOnReadReady(fd=channel.infd, handler=self.recvReady)
            return

    # create a node
    pdbg.log("instantiating my node")
    parent = node(name="parent", channel=channel)
    
    # register my 'sendReload' to be invoked when the pipe is channel is ready for write
    # watch for events
    pdbg.log("entering event loop")
    parent.dispatcher.watch()
    # wait for it to die
    pid, status = os.wait()
    pdbg.log("waiting for child to die")
    # check the pid
    pdbg.log("checking pid")
    assert pid == childpid
    # check the status
    code = (status & 0xF0)
    reason = status & 0x0F
    pdbg.log("checking the status: code={}, reason={}".format(code, reason))
    assert code == 0 and reason == 0
    pdbg.log("exiting")

    # all done
    return parent


# the child behavior
def onChild(channel):
    """
    The child enters an indefinite loop by repeatedly scheduling an alarm. The modified {Node}
    overrides the 'reload' signal handler to send an acknowledgment to the parent, and goes
    back to its indefinite loop. Eventually, the parent sends a SIGTERM, which kills the child
    """
    
    # debug
    cdbg = journal.debug("child")
    # log
    cdbg.log("in the child process")

    # base class
    from pyre.ipc.Node import Node
    # subclass Node
    class node(Node):

        def sendReady(self, **unused):
            # log
            cdbg.log("sending 'ready'")
            # get it
            self.marshaller.send(item='ready', channel=self.channel)
            # don't reschedule this handler
            return False
            
        def sendReloaded(self, selector, descriptor):
            # send a message to the parent
            cdbg.log("sending 'reloaded' to my parent")
            self.marshaller.send(item="reloaded", channel=self.channel)
            # don't reschedule
            return False

        def alarm(self, **kwds):
            cdbg.log("  timeout")
            self.dispatcher.alarm(interval=10*self.dispatcher.second, handler=self.alarm)
            return

        def onReload(self, *unused):
            # schedule to send a message to the parent
            cdbg.log("schedule 'sendReloaded'")
            self.dispatcher.notifyOnWriteReady(fd=self.channel.outfd, handler=self.sendReloaded)
            # all done
            return

        def onTerminate(self, *unused):
            cdbg.log("marking clean exit and stopping the dispatcher")
            # mark me
            self.cleanExit = True
            # delegate
            return super().onTerminate(*unused)

        def __init__(self, channel, **kwds):
            super().__init__(**kwds)
            # my communication channel
            self.channel = channel
            # marker that my {onTerminate} was called
            self.cleanExit = False
            # set up an alarm to keep the process alive
            self.dispatcher.alarm(interval=10*self.dispatcher.second, handler=self.alarm)
            # let my parent know I am ready
            self.dispatcher.notifyOnWriteReady(fd=channel.outfd, handler=self.sendReady)
            # all done 
            return

    # instantiate
    cdbg.log("instantiating my node")
    child = node(name="child", channel=channel)
    # enter the event loop
    cdbg.log("entering the event loop")
    child.dispatcher.watch()
    # check that this is a clean exit
    assert child.cleanExit
    # return it 
    cdbg.log("exiting")
    return child


# main
if __name__ == "__main__":
    # progress logging
    import journal
    journal.debug("child").active = False
    journal.debug("parent").active = False
    # do...
    test()


# end of file 
