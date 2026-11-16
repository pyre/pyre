#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the journal device holds records until its alarm fires, and then publishes them
on the journal topic as one frame
"""

# externals
import json

# support
import journal

# the device under test
from pyre.http.Journal import Journal

# the stream framing
from pyre.http.EventStream import EventStream


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


# a stand-in hub that records what is published on it
class Hub:
    """
    The slice of the hub interface the journal device uses
    """

    # metamethods
    def __init__(self):
        # the publications, as (frame, topic) pairs
        self.published = []
        # all done
        return

    # interface
    def publish(self, event, topic="", coalesce=False):
        """
        Record the publication of {event} on {topic}
        """
        # remember it
        self.published.append((event, topic))
        # all done
        return


# a stand-in for the server the device publishes through
class Server:
    """
    The pieces of an http server the journal device consults
    """

    # the identification string responses stamp into their headers
    name = "pyre/test"
    # the stream framing
    eventStream = EventStream

    # metamethods
    def __init__(self):
        # the event loop
        self.dispatcher = Dispatcher()
        # the hub
        self.hub = Hub()
        # the number of change notifications
        self.changes = 0
        # all done
        return

    # interface
    def notifyChange(self):
        """
        Count the change notifications
        """
        # one more
        self.changes += 1
        # all done
        return


def listen(device):
    """
    Make {device} the journal's default device, and return the one it replaces
    """
    # the device in place
    previous = journal.chronicler.device
    # replace it
    journal.chronicler.device = device
    # and hand the old one back, so it can be restored
    return previous


def test():
    """
    Flush a burst of entries, fire the alarm, and check what was published
    """
    # the server
    server = Server()
    # the device
    device = Journal(server=server, latency=0.25)
    # install it
    previous = listen(device)
    # carefully
    try:
        # make a channel
        channel = journal.info("pyre.http.tests.batch")
        # say three things
        for word in ["one", "two", "three"]:
            # one at a time
            channel.log(word)
    # whatever happens
    finally:
        # restore the journal
        journal.chronicler.device = previous
    # nothing has been published yet
    assert server.hub.published == []
    # one alarm was armed, for the latency
    assert len(server.dispatcher.alarms) == 1
    # find it
    interval, call = server.dispatcher.alarms[0]
    # it waits for the latency
    assert interval == 0.25
    # fire it; it does not ask to be rescheduled
    assert call(timestamp=0) is None
    # one frame went out, on the journal topic
    assert len(server.hub.published) == 1
    # find it
    frame, topic = server.hub.published[0]
    # it went out on the journal topic
    assert topic == "journal"
    # carrying the whole burst
    payload = json.loads(frame.decode("utf-8").split("data: ", 1)[1])
    # in order
    assert [record["page"] for record in payload] == [["one"], ["two"], ["three"]]
    # with nothing pending, firing again publishes nothing
    call(timestamp=0)
    # leaves the publications as they were
    assert len(server.hub.published) == 1
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
