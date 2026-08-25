#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a deferred response parks the connection and delivers its document on resolution
"""

# the server under test
from pyre.http.Server import Server

# the document that eventually gets delivered
from pyre.http.documents import OK

# the transport that stands in for the client connection
import pyre.ipc

# to peek at the wire without blocking
import select


# a document that carries a body, so the delivery has something recognizable to ship
class Page(OK):
    """
    An {OK} response with a fixed payload
    """

    # hand back a known body
    def render(self, **kwds):
        """
        Generate the payload
        """
        # a fixed page
        return b"<html>hi</html>"


def test():
    # build a server; no port is bound until activation, which this test never triggers
    server = Server(name="test.http.deferred")
    # and a connection, with the parent end playing the server side
    connection, client = pyre.ipc.newSocket().open()

    # make a response placeholder
    deferred = server.deferred()
    # hand it to the server in place of a document
    parked = server.respond(channel=connection, request=None, response=deferred)
    # the server keeps the connection open
    assert parked is True
    # and has installed its delivery hook
    assert deferred.deliver is not None
    # without writing anything to the wire yet
    ready, _, _ = select.select([client], [], [], 0)
    assert not ready

    # now the actual document becomes available
    page = Page(server=server)
    # deliver it
    deferred.resolve(response=page)
    # the client receives a complete response
    wire = client.read(minlen=15)
    # with the status line
    assert wire.startswith(b"HTTP/1.1 200 OK\r\n")
    # and the body
    assert wire.endswith(b"<html>hi</html>")

    # all done
    return server


# main
if __name__ == "__main__":
    test()


# end of file
