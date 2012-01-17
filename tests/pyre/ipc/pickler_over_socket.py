#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Build two processes that communicate using pickler over a pair of sockets

The server process acquires a port, to which it listens for incoming connections; the client
connects to this port and the two exchange a couple of simple messages.

In order to inform the client about the port number, and to avoid other synchronization
problems, the test case builds a pipe between the client and the server. The client waits for
data to come over its end of the pipe. The server acquires a port, and then communicates the
port number to the client through the pipe. The client sends a simple message, whic the server
receives and validates. It responds with a simple message of its own and shuts down its socket
and its pipe. The client receives its message, validates and exits.
"""

# externals
import os
# access the pyre ipc package
import pyre.ipc

def test():
    # make a pickler
    m = pyre.ipc.pickler()
    # and a pair of pipes
    parent, child = pyre.ipc.pipe.open()

    # fork
    pid = os.fork()
    # in the parent process
    if pid > 0:
        # invoke the parent behavior
        return onServer(marshaller=m, pipe=parent)
    # in the child, become the client
    return onClient(marshaller=m, pipe=child)


# the greetings
hello = "hello"
goodbye = "goodbye"
    

def onServer(marshaller, pipe):
    """Send a simple message and wait for the response"""

    # build an address
    address = pyre.ipc.socket.ipv4()

    # build my socket
    import socket
    l = socket.socket(address.family, socket.SOCK_STREAM)
    l.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    l.bind(address.value)
    l.listen(socket.SOMAXCONN)
    # find out what it was bound to
    host, port = l.getsockname()
    # print it
    print("server: port={}".format(port))
    # send it in a message to the client
    marshaller.send(item=port, channel=pipe)
    # and wait for an incoming connection
    incoming, peer = l.accept()
    # convert it to channel
    sock = pyre.ipc.socket(socket=incoming)

    # get the message
    message = marshaller.recv(channel=sock)
    print("server: message={!r}".format(message))
    # check it
    assert message == hello
    # say goodbye
    marshaller.send(item=goodbye, channel=sock)

    # shut everything down
    l.close()

    # all done
    return


def onClient(marshaller, pipe):
    """Wait for a message and send a response"""
    # get the port number
    port = marshaller.recv(channel=pipe)
    # print it
    print("client: port={}".format(port))
    # convert it into an address
    address = pyre.ipc.socket.ipv4(port=port)
    # make a channel
    sock = pyre.ipc.socket.open(address)
    # send a message
    marshaller.send(item=hello, channel=sock)
    # get the response
    response = marshaller.recv(channel=sock)
    print("client: response={!r}".format(response))
    # check it
    assert response == goodbye

    # all done
    return
    
    
# main
if __name__ == "__main__":
    test()


# end of file 
