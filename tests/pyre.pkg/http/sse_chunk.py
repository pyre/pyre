#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that {EventStream} wraps bytes as chunks of a body in the chunked transfer coding: the
size in hex, a line break, the payload, a line break; and that it never emits the empty chunk,
which would tell the peer that the stream is over
"""

# the source of the coding
from pyre.http.EventStream import EventStream


def test():
    # a short payload
    assert EventStream.chunk(b"abc") == b"3\r\nabc\r\n"
    # the size is in hex
    assert EventStream.chunk(b"x" * 255) == b"ff\r\n" + b"x" * 255 + b"\r\n"
    # the payload is opaque: line breaks of its own are counted, not interpreted
    assert EventStream.chunk(b"data: 1\n\n") == b"9\r\ndata: 1\n\n\r\n"
    # the keep-alive frame wraps like any other
    assert EventStream.chunk(EventStream.keepalive()) == b"d\r\n: keepalive\n\n\r\n"
    # a chunk of no bytes terminates the body, so an empty payload contributes nothing
    assert EventStream.chunk(b"") == b""

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
