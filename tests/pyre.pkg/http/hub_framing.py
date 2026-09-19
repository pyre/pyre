#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the http {Hub} wraps what it delivers to a subscriber in the transfer coding of its
connection: every delivery is wrapped exactly once, even across partial sends, raw deliveries
bypass the coding, identical wrapped frames still coalesce, the keep-alive is wrapped as well,
and subscribers without a coding get their bytes as they are
"""

# the registry under test
from pyre.http.Hub import Hub

# the source of the coding
from pyre.http.EventStream import EventStream


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
    # the coding under test
    chunk = EventStream.chunk

    # every delivery is wrapped, except the ones marked raw
    # a fresh dispatcher and hub
    dispatcher = Dispatcher()
    hub = Hub(dispatcher=dispatcher)
    # a channel that accepts everything
    channel = Channel()
    # subscribe it to a topic, with the chunked coding
    hub.subscribe(channel=channel, topic="t", framing=chunk)
    # the part of the response that precedes the body goes out as it is
    hub.send(channel=channel, data=b"preamble", raw=True)
    # a direct delivery is part of the body
    hub.send(channel=channel, data=b"opening")
    # and so is a published event
    hub.publish(b"event", topic="t")
    # drain the queue
    assert hub.flush(channel=channel) is False
    # the preamble is untouched, and each body delivery is a chunk of its own
    assert channel.buffer == b"preamble" + b"7\r\nopening\r\n" + b"5\r\nevent\r\n"

    # a chunk that does not fit in one send is wrapped once, not once per attempt
    # a fresh dispatcher and hub
    dispatcher = Dispatcher()
    hub = Hub(dispatcher=dispatcher)
    # a channel that takes only four bytes per send
    channel = Channel(limit=4)
    # subscribe it to the default topic, with the chunked coding
    hub.subscribe(channel=channel, framing=chunk)
    # queue six bytes
    hub.send(channel=channel, data=b"abcdef")
    # flush until the queue drains
    while hub.flush(channel=channel):
        # each pass takes what fits
        pass
    # the wire carries exactly one chunk
    assert channel.buffer == b"6\r\nabcdef\r\n"

    # identical frames still coalesce, since identical payloads wrap identically
    # a fresh dispatcher and hub
    dispatcher = Dispatcher()
    hub = Hub(dispatcher=dispatcher)
    # a channel that accepts everything
    channel = Channel()
    # subscribe it to the default topic, with the chunked coding
    hub.subscribe(channel=channel, framing=chunk)
    # publish the same notification twice, coalescing
    hub.publish(b"change", coalesce=True)
    hub.publish(b"change", coalesce=True)
    # drain the queue
    assert hub.flush(channel=channel) is False
    # only one made it to the wire
    assert channel.buffer == b"6\r\nchange\r\n"

    # the keep-alive is part of the body, so it is wrapped as well
    # a fresh dispatcher and a hub with a heartbeat
    dispatcher = Dispatcher()
    hub = Hub(dispatcher=dispatcher, interval=1, keepalive=b"ping")
    # a channel that accepts everything
    channel = Channel()
    # subscribe it to the default topic, with the chunked coding; this starts the timer
    hub.subscribe(channel=channel, framing=chunk)
    # get the handler of the alarm
    _, heartbeat = dispatcher.alarms[0]
    # fire it
    heartbeat(timestamp=0)
    # drain the queue
    assert hub.flush(channel=channel) is False
    # the keep-alive arrived as a chunk
    assert channel.buffer == b"4\r\nping\r\n"

    # a subscriber without a coding sits next to one with, and each gets its own treatment
    # a fresh dispatcher and hub
    dispatcher = Dispatcher()
    hub = Hub(dispatcher=dispatcher)
    # two channels that accept everything
    plain = Channel()
    chunked = Channel()
    # subscribe one as it has always been done
    hub.subscribe(channel=plain, topic="t")
    # and the other with the chunked coding
    hub.subscribe(channel=chunked, topic="t", framing=chunk)
    # publish an event to both
    hub.publish(b"event", topic="t")
    # drain the queues
    assert hub.flush(channel=plain) is False
    assert hub.flush(channel=chunked) is False
    # the first got the bytes as they are
    assert plain.buffer == b"event"
    # and the second got a chunk
    assert chunked.buffer == b"5\r\nevent\r\n"

    # unsubscribing forgets the coding
    hub.unsubscribe(chunked)
    # so nothing of the channel lingers
    assert chunked not in hub._framings

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
