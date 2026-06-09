#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify the http {Hub} arms a channel exactly once, drains with partial sends, re-arms once its
queue empties, and cleans up on unsubscribe
"""

# the registry under test
from pyre.http.Hub import Hub


# a stand-in dispatcher that records every channel armed for write-readiness
class Dispatcher:
    """
    The slice of the dispatcher interface the hub uses
    """

    # meta-methods
    def __init__(self):
        # start with an empty record of armings
        self.armed = []
        # all done
        return

    # the only dispatcher method the hub calls
    def whenWriteReady(self, channel, call):
        """
        Record that {channel} was armed with the {call} handler
        """
        # remember the arming so the test can count it
        self.armed.append((channel, call))
        # all done
        return


# a stand-in channel whose socket accepts at most {limit} bytes per send ({None} accepts all)
class Channel:
    """
    A socket-like endpoint with a controllable per-send capacity
    """

    # meta-methods
    def __init__(self, limit=None):
        # the bytes delivered so far
        self.buffer = b""
        # how many bytes a single send will accept
        self.limit = limit
        # all done
        return

    # accept up to {limit} bytes, like a non-blocking socket with a nearly-full buffer
    def send(self, data):
        """
        Accept up to {limit} bytes of {data} and report how many were taken
        """
        # decide how many bytes to take
        n = len(data) if self.limit is None else min(self.limit, len(data))
        # append exactly that many
        self.buffer += data[:n]
        # and report the count, as a real socket does
        return n


def test():
    # arm exactly once across publishes, then drain fully
    # a fresh dispatcher and hub
    dispatcher = Dispatcher()
    hub = Hub(dispatcher=dispatcher)
    # a channel that accepts everything
    channel = Channel()
    # subscribe it to a topic
    hub.subscribe(channel=channel, topic="t")
    # publish two events to that topic
    hub.publish(b"one", topic="t")
    hub.publish(b"two", topic="t")
    # the two publishes armed the channel exactly once
    assert len(dispatcher.armed) == 1
    # a flush delivers both frames and reports the queue is now empty
    assert hub.flush(channel=channel) is False
    # the channel received them concatenated, in order
    assert channel.buffer == b"one" + b"two"
    # and it is no longer armed
    assert channel not in hub._armed

    # a frame larger than one send is delivered across flushes
    # a fresh dispatcher and hub
    dispatcher = Dispatcher()
    hub = Hub(dispatcher=dispatcher)
    # a channel that takes only three bytes per send
    channel = Channel(limit=3)
    # subscribe it to the default topic
    hub.subscribe(channel=channel)
    # queue six bytes
    hub.send(channel=channel, data=b"abcdef")
    # the first flush takes what fits, keeps the rest, and asks to be rescheduled
    assert hub.flush(channel=channel) is True
    # three bytes made it through
    assert channel.buffer == b"abc"
    # and the channel is still armed for the remainder
    assert channel in hub._armed
    # the second flush delivers the rest and disarms
    assert hub.flush(channel=channel) is False
    # all six bytes are now through
    assert channel.buffer == b"abcdef"
    # and the channel is disarmed
    assert channel not in hub._armed

    # a publish after the queue empties arms the channel afresh
    # remember how many armings we have seen
    before = len(dispatcher.armed)
    # publish once more
    hub.publish(b"z")
    # which arms the channel again
    assert len(dispatcher.armed) == before + 1

    # unsubscribe forgets the channel; a later send to it is a quiet no-op
    # drop the channel
    hub.unsubscribe(channel)
    # its queue is gone
    assert channel not in hub._queues
    # its armed flag is gone
    assert channel not in hub._armed
    # and sending to it now does nothing, rather than raising
    hub.send(channel=channel, data=b"x")

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
