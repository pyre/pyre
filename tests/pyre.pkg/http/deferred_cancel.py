#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a peer hangup cancels the response parked on its connection, and that delivery
clears the parking registry
"""

# externals
import journal

# the server under test
from pyre.http.Server import Server

# the document that gets delivered in the happy case
from pyre.http.documents import OK

# the transport that stands in for the client connection
import pyre.ipc


# the minimal application surface the server consults while processing traffic
class App:
    """
    A stand-in for the hosting application
    """

    # the diagnostic channel the server logs to
    debug = journal.debug("test.http.cancel")


# a document that carries a body
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
    server = Server(name="test.http.deferred.cancel")
    # give it an application to talk to
    server.application = App()

    # the hangup scenario
    connection, client = pyre.ipc.newSocket().open()
    # make a response placeholder
    deferred = server.deferred()
    # the record of cancellations
    fired = []
    # install the producer's cancellation hook
    deferred.abandoned = lambda: fired.append(True)
    # park it
    assert server.respond(channel=connection, request=None, response=deferred) is True
    # the server remembers the parked response
    assert server.parked[connection] is deferred
    # the peer hangs up
    client.close()
    # the server processes the hangup
    keep = server.process(channel=connection)
    # and stops watching the connection
    assert keep is False
    # the producer heard about it
    assert fired == [True]
    # and the parking registry is clean
    assert connection not in server.parked

    # the happy scenario: delivery also clears the registry
    connection, client = pyre.ipc.newSocket().open()
    # park a fresh placeholder
    deferred = server.deferred()
    server.respond(channel=connection, request=None, response=deferred)
    assert connection in server.parked
    # the document becomes available and is delivered
    deferred.resolve(response=Page(server=server))
    # the registry is clean
    assert connection not in server.parked
    # and the client received the response
    wire = client.read(minlen=15)
    assert wire.startswith(b"HTTP/1.1 200 OK\r\n")
    assert wire.endswith(b"<html>hi</html>")

    # all done
    return server


# main
if __name__ == "__main__":
    test()


# end of file
