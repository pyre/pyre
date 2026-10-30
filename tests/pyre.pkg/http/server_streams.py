#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the event stream opens with the greeting, and that the journal stream opens with
the greeting followed by the history
"""

# support
import journal

# the server under test
from pyre.http.Server import Server

# the event hub
from pyre.http.Hub import Hub


# a stand-in dispatcher that records the alarms and the write registrations it is asked for
class Dispatcher:
    """
    The slice of the dispatcher interface the hub and the journal device use
    """

    # metamethods
    def __init__(self):
        # the alarms scheduled, as (interval, handler) pairs
        self.alarms = []
        # the channels armed for write-readiness
        self.armed = []
        # all done
        return

    # interface
    def alarm(self, interval, call):
        """
        Record that {call} should fire after {interval}
        """
        # remember it
        self.alarms.append((interval, call))
        # all done
        return

    def whenWriteReady(self, channel, call):
        """
        Record that {channel} was armed with the {call} handler
        """
        # remember it
        self.armed.append((channel, call))
        # all done
        return


def test():
    """
    Open both streams and check their topics and openings
    """
    # a server
    server = Server(name="pyre.http.tests.streams")
    # with a token, an event loop, a hub, and a journal device, as activation would set them up
    server.instance = "a-token"
    server.dispatcher = Dispatcher()
    server.hub = Hub(dispatcher=server.dispatcher)
    # the device in place, which the test keeps quiet so its entry does not reach the terminal
    terminal = journal.chronicler.device
    # replaced by a silent one
    journal.chronicler.device = journal.trash()
    # install the server's device over it
    server._listen()
    # carefully
    try:
        # say something
        journal.info("pyre.http.tests.streams").log("hello")
        # open the journal stream
        chronicle = server.chronicle()
    # whatever happens
    finally:
        # hand the journal back
        server.shutdown()
        # and restore the terminal
        journal.chronicler.device = terminal
    # the journal stream is on the journal topic
    assert chronicle.topic == "journal"
    # the greeting
    greeting = server.hello()
    # opens it
    assert chronicle.opening.startswith(greeting)
    # and what follows
    history = chronicle.opening[len(greeting) :].decode("utf-8")
    # is a batch of records
    assert history.startswith("event: journal\n")
    # holding what was said
    assert '"hello"' in history
    # the event stream
    events = server.events()
    # is on the global topic
    assert events.topic == ""
    # and opens with the greeting alone
    assert events.opening == greeting
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
