#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify the {EventStream} response frames SSE correctly and carries the SSE headers
"""

# the response under test
from pyre.http.EventStream import EventStream


# a stand-in for the server; the {Response} base only consults it for its {name}
class Server:
    """
    The minimal server surface a response needs
    """

    # the identification string the response stamps into its headers
    name = "pyre/test"


def test():
    # build a stream scoped to the {updates} topic
    stream = EventStream(server=Server(), topic="updates")

    # it routes down the server's streaming path
    assert stream.streaming is True
    # it holds the connection open
    assert stream.alive is True
    # it is a successful response
    assert stream.code == 200
    # it remembers the topic that scopes its delivery
    assert stream.topic == "updates"

    # it advertises the SSE content type
    assert stream.headers["Content-Type"] == "text/event-stream"
    # it forbids caching of the stream
    assert stream.headers["Cache-Control"] == "no-cache"
    # it asks intermediaries to keep the connection open
    assert stream.headers["Connection"] == "keep-alive"
    # and it opts out of reverse-proxy buffering, so events are not held back
    assert stream.headers["X-Accel-Buffering"] == "no"

    # a bare payload frames as a single {data} line terminated by a blank line
    assert stream.event("hello") == b"data: hello\n\n"
    # the optional fields render in order, and multi-line data splits across {data} lines so the
    # embedded newline stays inside this one frame
    assert stream.event("a\nb", name="change", id=7, retry=3000) == (
        b"id: 7\nevent: change\nretry: 3000\ndata: a\ndata: b\n\n"
    )
    # a streaming response renders no body of its own
    assert stream.render() == b""

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
