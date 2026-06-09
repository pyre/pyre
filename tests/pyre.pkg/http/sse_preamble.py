#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify the {HTTP} renderer's {preamble} emits the server-sent events preamble: the status line
and the full set of SSE headers, with no {Content-Length} and no body
"""

# the renderer under test
from pyre.weaver.HTTP import HTTP
# the streaming response it renders
from pyre.http.EventStream import EventStream


# a stand-in for the server; the {Response} base only consults it for its {name}
class Server:
    """
    The minimal server surface a response needs
    """

    # the identification string the response stamps into its headers
    name = "pyre/test"


def test():
    # build the renderer and a streaming response
    renderer = HTTP(name="renderer")
    stream = EventStream(server=Server(), topic="updates")

    # the server frames the preamble by joining the fragments and ending the header block itself
    wire = b"\r\n".join(renderer.preamble(document=stream)) + b"\r\n\r\n"

    # the status line opens the response
    assert wire.startswith(b"HTTP/1.0 200 OK\r\n")
    # the SSE content type rides along
    assert b"Content-Type: text/event-stream\r\n" in wire
    # the stream forbids caching
    assert b"Cache-Control: no-cache\r\n" in wire
    # it asks intermediaries to hold the connection open
    assert b"Connection: keep-alive\r\n" in wire
    # and it opts out of reverse-proxy buffering, so events are not held back
    assert b"X-Accel-Buffering: no\r\n" in wire
    # a streaming response has no body, so it carries no {Content-Length}
    assert b"Content-Length" not in wire
    # the preamble is exactly the status line and headers, terminated by a blank line
    assert wire.endswith(b"\r\n\r\n")

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
