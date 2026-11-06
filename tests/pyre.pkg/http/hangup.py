#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a response that hangs up closes the connection without sending anything, and that the
server forgets the conversation on it
"""

# the server under test
from pyre.http.Server import Server

# the response that hangs up
from pyre.http.responses import NoResponse

# the transport that stands in for the client connection
import pyre.ipc


def test():
    # build a server; no port is bound until activation, which this test never triggers
    server = Server(name="test.http.hangup")
    # and a connection, with the parent end playing the server side
    connection, client = pyre.ipc.newSocket().open()
    # a request that was still arriving on it
    server.requests[connection] = object()

    # respond by hanging up
    alive = server.respond(channel=connection, request=None, response=NoResponse(server=server))

    # the server stops listening to the connection
    assert alive is False
    # forgets the request
    assert connection not in server.requests
    # and the client reads the end of the stream, with nothing before it
    assert client.read(maxlen=4096) == b""

    # all done
    return server


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
