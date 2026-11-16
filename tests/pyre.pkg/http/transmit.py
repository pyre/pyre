#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a response whose body is in a file is sent straight from the file, with its size as
the content length, and that the server closes the file once it is on the wire
"""

# the server under test
from pyre.http.Server import Server

# the document that carries the file
from pyre.http.documents import BMP

# the transport that stands in for the client connection
import pyre.ipc

# for the file that holds the body
import tempfile

# the client reads while the server writes
import threading


def test():
    # build a server; no port is bound until activation, which this test never triggers
    server = Server(name="test.http.transmit")
    # and a connection, with the parent end playing the server side
    connection, client = pyre.ipc.newSocket().open()

    # a body larger than the buffers of the connection, so it goes out in several pieces
    body = bytes(range(256)) * 1024
    # parked in a file
    payload = tempfile.TemporaryFile()
    # that holds the body
    payload.write(body)
    # and nothing else
    payload.flush()

    # the preamble and the body, as the client receives them
    wire = []

    # the client
    def receive():
        """
        Read the whole response
        """
        # enough to hold the preamble and the body
        wire.append(client.read(minlen=len(body) + 100, maxlen=len(body) + 4096))
        # all done
        return

    # start reading before the server writes, since the server blocks until the body is sent
    reader = threading.Thread(target=receive)
    reader.start()
    # the document
    document = BMP(server=server, payload=payload)
    # respond with it
    alive = server.respond(channel=connection, request=None, response=document)
    # close the server end, so the client sees the end of the response
    connection.close()
    # wait for the client
    reader.join()

    # the server keeps the connection alive, the way it does after any other document
    assert alive is True
    # and has closed the file
    assert payload.closed
    # split the response at the end of the headers
    preamble, _, received = wire[0].partition(b"\r\n\r\n")
    # the status line
    assert preamble.startswith(b"HTTP/1.1 200 OK\r\n")
    # announces the size of the body
    assert f"Content-Length: {len(body)}".encode() in preamble
    # and the body is intact
    assert received == body

    # all done
    return server


# main
if __name__ == "__main__":
    test()


# end of file
