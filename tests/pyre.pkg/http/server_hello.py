#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the greeting that opens every event stream is named, and carries the token of
this run of the server
"""

# support
import json

# the server under test
from pyre.http.Server import Server

# the event hub
from pyre.http.Hub import Hub


def test():
    """
    Build the greeting and check its name, payload, and permanence
    """
    # a server
    server = Server(name="pyre.http.tests.hello")
    # with a token, as activation would mint it
    server.instance = "a-token"
    # the greeting
    frame = server.hello()
    # is named
    text = frame.decode("utf-8")
    # under the name of the greeting
    assert text.startswith("event: hello\n")
    # carries the token
    payload = json.loads(text.split("data: ", 1)[1])
    # which is the token
    assert payload == {"instance": "a-token"}
    # and is built once
    assert server.hello() is frame
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
