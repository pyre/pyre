#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the server installs its journal device over the one in place, and gives the
journal back to that device at shutdown
"""

# support
import journal

# the server under test
from pyre.http.Server import Server

# the event hub
from pyre.http.Hub import Hub

# the device it installs
from pyre.http.Journal import Journal


# a stand-in dispatcher that the hub can hold
class Dispatcher:
    """
    The dispatcher, as far as building a hub is concerned
    """


def test():
    """
    Install the device, then shut down, and check the journal's device each time
    """
    # the device in place
    terminal = journal.chronicler.device
    # a server
    server = Server(name="pyre.http.tests.shutdown")
    # with a hub, as activation would build it
    server.hub = Hub(dispatcher=Dispatcher())
    # install its device
    server._listen()
    # carefully
    try:
        # the journal writes to the server's device
        assert isinstance(journal.chronicler.device, Journal)
        # which mirrors the device it replaced
        assert server.journal.mirror is terminal
    # whatever happens
    finally:
        # shut down
        server.shutdown()
    # the journal writes to the original device again
    assert journal.chronicler.device is terminal
    # and the server has let go of its own
    assert server.journal is None
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
