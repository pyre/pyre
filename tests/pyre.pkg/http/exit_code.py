#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify {code} (the HTTP status) and {exitCode} (the shell exit code) are distinct: {Exit} renders
a 200 status yet terminates the process with its own {exitCode}, while every other document type
leaves {exitCode} at the default 0
"""

# the server that drives the response path
from pyre.http.Server import Server
# the document types under test
from pyre.http import documents


# a stand-in client connection that records whatever the server writes
class Channel:
    """
    A write sink that captures the bytes the server sends
    """

    # meta-methods
    def __init__(self):
        # the bytes written so far
        self.data = b""
        # all done
        return

    # accept and record a write
    def write(self, data):
        """
        Record {data} and report all of it as accepted
        """
        # capture it
        self.data += data
        # and report the whole write went through
        return len(data)


def test():
    # a server to render and serve the response
    server = Server(name="exit-code-test")

    # an Exit carrying a non-default shell exit code
    response = documents.Exit(server=server, exitCode=42)
    # a channel to capture the rendered preamble
    channel = Channel()
    # serving an aborting response renders it and then terminates the process
    try:
        # which raises {SystemExit}
        server.respond(channel=channel, request=None, response=response)
    # catch it
    except SystemExit as error:
        # the shell exit code is the response's {exitCode}, not its HTTP status
        assert error.code == 42
    # if it did not raise
    else:
        # the abort path is broken
        assert False
    # and what reached the client is a well-formed 200 status line: the HTTP {code} is untouched
    assert channel.data.startswith(b"HTTP/1.1 200 OK\r\n")

    # the exit code defaults to a clean 0 when none is requested
    assert documents.Exit(server=server).exitCode == 0

    # every other document type leaves {exitCode} at the default 0; only {Exit} overrides it
    for entity in vars(documents).values():
        # skip non-classes and names imported from elsewhere
        if not isinstance(entity, type) or entity.__module__ != documents.__name__:
            # not one of ours
            continue
        # Exit is the one type that carries a custom exit code
        if entity is documents.Exit:
            # so it is exempt
            continue
        # all the others inherit the default
        assert entity.exitCode == 0

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
