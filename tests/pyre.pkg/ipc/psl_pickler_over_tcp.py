#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise a PSL selector watching over file sockets
"""

# externals
import pyre
import journal
import os

# setup a couple of journal channels
serverdbg = journal.debug("selector.server")
# serverdbg.active = True
clientdbg = journal.debug("selector.client")
# clientdbg.active = True


def test():
    # build the marshaler
    m = pyre.ipc.newPickler()
    # and the communication channels
    server, client = pyre.ipc.pipe()

    # fork
    pid = os.fork()
    # in the server process
    if pid > 0:
        # invoke the server behavior
        return onServer(clientPid=pid, marshaler=m, pipe=client)

    # in the client process
    # get my pid
    clientPid = os.getpid()
    # invoke the behavior
    return onClient(clientPid=clientPid, marshaler=m, pipe=server)


def onServer(clientPid, marshaler, pipe):
    # observe the server selector at work
    # journal.debug("pyre.ipc.selector").active = True

    # build my selector
    serverdbg.log("server: building a selector")
    s = pyre.ipc.newPSL()

    # establish a network presence
    port = pyre.ipc.port()
    # report what it was bound to
    serverdbg.log(f"server: listening at {port.address}")

    def getMessage(channel, **kwds):
        message = marshaler.recv(channel)
        serverdbg.log(f"server: received '{message}'")
        # check it
        assert message == f"Hello from {clientPid}"
        return False

    def sendAddress(channel, **kwds):
        serverdbg.log(f"server: sending address {port.address}")
        marshaler.send(channel=channel, item=port.address)
        serverdbg.log("server: done sending address")
        return False

    def connectionAttempt(channel, **kwds):
        peer, address = channel.accept()
        serverdbg.log(f"server: connection attempt from {address}")
        serverdbg.log(f"server: scheduling a reader for {peer}")
        # schedule the receiving of the message
        s.whenReadReady(channel=peer, call=getMessage)
        # and stop waiting for any further connections
        return False

    def alarm(timestamp):
        print(f"alarm: {timestamp}")
        return 1 * pyre.units.SI.second

    # let me know when the pipe to the client is ready for writing so i can send my port
    serverdbg.log("server: registering the port notification routine")
    s.whenWriteReady(channel=pipe, call=sendAddress)
    serverdbg.log("server: registering the connection routine")
    s.whenReadReady(channel=port, call=connectionAttempt)

    # set up an alarm
    # s.alarm(interval=2 * pyre.units.SI.second, call=alarm)

    # invoke the selector
    serverdbg.log("server: entering watch")
    s.watch()
    serverdbg.log("server: all done")

    # all done
    return


def onClient(clientPid, marshaler, pipe):
    # observe the client selector at work
    # journal.debug("pyre.ipc.selector").active = True

    # build my selector
    clientdbg.log("client: building a selector")
    s = pyre.ipc.newPSL()

    # the port notification routine
    def recvAddress(channel, **kwds):
        # get the port
        clientdbg.log("client: receiving address")
        address = marshaler.recv(channel)
        clientdbg.log(f"client: address={address}")

        # make a connection
        tcp = pyre.ipc.tcp(address=address)
        # send a message
        message = f"Hello from {clientPid}"
        clientdbg.log(f"client: sending '{message}'")
        marshaler.send(channel=tcp, item=message)
        # all done
        return False

    # let me know when the pipe to the client is ready for writing so i can send my port
    clientdbg.log("client: registering the port notification routine")
    s.whenReadReady(channel=pipe, call=recvAddress)

    # invoke the selector
    clientdbg.log("client: entering watch")
    s.watch()
    clientdbg.log("client: all done")

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
