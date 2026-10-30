#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that change notifications go out on the global topic and that a burst of them leaves
one frame queued for a subscriber
"""

# support
import json

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
    Notify twice and check the subscriber's queue
    """
    # a server
    server = Server(name="pyre.http.tests.notify")
    # with a hub, as activation would build it
    server.hub = Hub(dispatcher=Dispatcher())
    # a subscriber to the global topic
    channel = object()
    # joins the global topic
    server.hub.subscribe(channel=channel)
    # notify twice
    server.notifyChange()
    # and again, right away
    server.notifyChange()
    # one frame is queued
    queue = server.hub._queues[channel]
    # holds one frame
    assert len(queue) == 1
    # an unnamed change notification
    assert json.loads(queue[0].decode("utf-8").split("data: ", 1)[1]) == {"type": "change"}
    # with no name, so clients treat it as a change
    assert b"event:" not in queue[0]
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
