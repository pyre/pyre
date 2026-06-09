#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify the http {Hub}: it arms a channel once, drains with partial sends, re-arms once empty,
cleans up on unsubscribe, coalesces identical frames, drops a subscriber that overflows its queue,
and broadcasts a recurring keep-alive while it has subscribers
"""

# the registry under test
from pyre.http.Hub import Hub


# a stand-in dispatcher that records every channel armed for write-readiness and every alarm set
class Dispatcher:
    """
    The slice of the dispatcher interface the hub uses
    """

    # meta-methods
    def __init__(self):
        # the channels armed for write-readiness
        self.armed = []
        # the alarms scheduled, as (interval, handler) pairs
        self.alarms = []
        # all done
        return

    # arm a channel for write-readiness
    def whenWriteReady(self, channel, call):
        """
        Record that {channel} was armed with the {call} handler
        """
        # remember the arming so the test can count it
        self.armed.append((channel, call))
        # all done
        return

    # schedule a timer
    def alarm(self, interval, call):
        """
        Record that an alarm was scheduled to fire {call} after {interval}
        """
        # remember the alarm so the test can drive it
        self.alarms.append((interval, call))
        # all done
        return


# a stand-in channel whose socket accepts at most {limit} bytes per send ({None} accepts all)
class Channel:
    """
    A socket-like endpoint with a controllable per-send capacity that records when it is closed
    """

    # meta-methods
    def __init__(self, limit=None):
        # the bytes delivered so far
        self.buffer = b""
        # how many bytes a single send will accept
        self.limit = limit
        # whether the channel has been closed
        self.closed = False
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

    # close the connection
    def close(self):
        """
        Mark the channel as closed
        """
        # note the closure
        self.closed = True
        # all done
        return


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

    # coalescing skips an identical frame already pending at the tail
    # a fresh dispatcher and hub
    dispatcher = Dispatcher()
    hub = Hub(dispatcher=dispatcher)
    # a channel
    channel = Channel()
    # subscribe it
    hub.subscribe(channel=channel)
    # publish the same frame twice, coalescing
    hub.publish(b"same", coalesce=True)
    hub.publish(b"same", coalesce=True)
    # only one copy is pending
    assert len(hub._queues[channel]) == 1
    # a different frame is still queued
    hub.publish(b"other", coalesce=True)
    assert len(hub._queues[channel]) == 2

    # a subscriber that overflows its queue is dropped and closed
    # a hub that holds at most two frames per subscriber
    dispatcher = Dispatcher()
    hub = Hub(dispatcher=dispatcher, capacity=2)
    # a channel that never drains (its socket is not flushed during this block)
    channel = Channel()
    # subscribe it
    hub.subscribe(channel=channel)
    # fill the queue to capacity
    hub.send(channel=channel, data=b"a")
    hub.send(channel=channel, data=b"b")
    # the queue is full
    assert len(hub._queues[channel]) == 2
    # the next send overflows, so the subscriber is dropped and its connection closed
    hub.send(channel=channel, data=b"c")
    # it is gone from the hub
    assert channel not in hub._queues
    # and its connection was closed
    assert channel.closed is True

    # the keep-alive heartbeat runs while there are subscribers and lapses when there are none
    # a hub configured with a keep-alive frame and an interval
    dispatcher = Dispatcher()
    hub = Hub(dispatcher=dispatcher, keepalive=b": keepalive\n\n", interval=1)
    # before anyone subscribes, no timer is scheduled
    assert len(dispatcher.alarms) == 0
    # the first subscriber starts the timer
    first = Channel()
    hub.subscribe(channel=first)
    assert len(dispatcher.alarms) == 1
    # a second subscriber does not start a second timer
    second = Channel()
    hub.subscribe(channel=second)
    assert len(dispatcher.alarms) == 1
    # firing the timer broadcasts the keep-alive to every subscriber and asks to recur
    interval, beat = dispatcher.alarms[0]
    assert beat(timestamp=0) == 1
    # each subscriber has the keep-alive queued
    assert hub._queues[first][-1] == b": keepalive\n\n"
    assert hub._queues[second][-1] == b": keepalive\n\n"
    # with no subscribers left, the next tick declines to recur
    hub.unsubscribe(first)
    hub.unsubscribe(second)
    assert beat(timestamp=0) is None
    # and a fresh subscription restarts the timer
    third = Channel()
    hub.subscribe(channel=third)
    assert len(dispatcher.alarms) == 2

    # unsubscribe touches only the leaving channel's topics and prunes the ones left empty
    # a fresh dispatcher and hub
    dispatcher = Dispatcher()
    hub = Hub(dispatcher=dispatcher)
    # one channel on topic "x", another on topic "y"
    here = Channel()
    there = Channel()
    hub.subscribe(channel=here, topic="x")
    hub.subscribe(channel=there, topic="y")
    # drop the first
    hub.unsubscribe(here)
    # it is gone from the reverse index and its queue
    assert here not in hub._topics
    assert here not in hub._queues
    # its now-empty topic is pruned entirely
    assert "x" not in hub._subscribers
    # the other channel and its topic are untouched
    assert there in hub._subscribers["y"]
    assert hub._topics[there] == {"y"}

    # a channel on several topics is removed from all of them at once
    # a fresh dispatcher and hub
    dispatcher = Dispatcher()
    hub = Hub(dispatcher=dispatcher)
    # one channel joining two topics
    both = Channel()
    hub.subscribe(channel=both, topic="a")
    hub.subscribe(channel=both, topic="b")
    # the reverse index records both
    assert hub._topics[both] == {"a", "b"}
    # unsubscribe removes it from both and prunes both now-empty topics
    hub.unsubscribe(both)
    assert "a" not in hub._subscribers
    assert "b" not in hub._subscribers
    assert both not in hub._topics

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
