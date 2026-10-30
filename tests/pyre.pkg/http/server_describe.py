#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the server describes its process completely
"""

# externals
import os

# the server under test
from pyre.http.Server import Server


def test():
    """
    Describe a server before and after it has come up
    """
    # a server
    server = Server(name="pyre.http.tests.describe")
    # before it comes up
    description = server.describe()
    # every field is there
    assert set(description) == {
        "pid",
        "host",
        "platform",
        "cores",
        "memory",
        "started",
        "uptime",
        "descriptors",
        "ceiling",
    }
    # it is this process
    assert description["pid"] == os.getpid()
    # which has not started, so it has no uptime
    assert description["started"] is None
    # so it has no uptime
    assert description["uptime"] is None
    # once it comes up
    server.started = 0.0
    # it has been up for a while
    assert server.describe()["uptime"] > 0
    # it holds some descriptors, within its ceiling
    held = description["descriptors"]
    # within its ceiling, unless the platform cannot count them
    assert held is None or 0 < held <= description["ceiling"]
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
