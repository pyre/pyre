# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import collections


# the streaming subscriber registry and outbound pump
class Hub:
    """
    The registry of streaming subscribers and the pump that feeds them

    A {Hub} is owned by an HTTP server. It tracks the connections subscribed to each topic,
    buffers the bytes destined for each connection, and drains those buffers without blocking
    the server's event loop, riding the dispatcher's write-readiness notifications. It also
    broadcasts a periodic keep-alive so idle connections are not reaped by intermediaries, and
    it bounds each connection's buffer so a slow consumer cannot grow it without limit.
    """

    # interface
    def subscribe(self, channel, topic=""):
        """
        Record {channel} as a subscriber to {topic} and prepare its outbound queue
        """
        # add the channel to the topic's subscriber set
        self._subscribers[topic].add(channel)
        # make sure it has an outbound queue
        self._queues.setdefault(channel, collections.deque())
        # make sure the keep-alive timer is running, now that there is someone to feed
        self._beat()
        # all done
        return

    def unsubscribe(self, channel):
        """
        Drop {channel} from every topic, discard its queue, and forget it is armed
        """
        # remove it from each topic's subscriber set
        for subscribers in self._subscribers.values():
            # quietly, whether or not it is present
            subscribers.discard(channel)
        # discard its outbound queue
        self._queues.pop(channel, None)
        # and its armed flag
        self._armed.discard(channel)
        # all done
        return

    def publish(self, event, topic="", coalesce=False):
        """
        Append the {event} bytes to the outbound queue of every subscriber to {topic}

        When {coalesce} is set, an {event} identical to the one already pending at the tail of a
        subscriber's queue is skipped, so a burst of identical notifications collapses to one.
        """
        # iterate a snapshot of the subscribers: a send may drop an overflowing subscriber, which
        # mutates the set we would otherwise be iterating
        for channel in tuple(self._subscribers.get(topic, ())):
            # enqueue the event on each
            self.send(channel=channel, data=event, coalesce=coalesce)
        # all done
        return

    def send(self, channel, data, coalesce=False):
        """
        Append the {data} bytes to {channel}'s outbound queue and arm it for delivery

        When {coalesce} is set and {data} already sits at the tail of the queue, the append is
        skipped. A subscriber whose queue is full is dropped, so it reconnects and resynchronizes
        rather than growing the buffer without bound.
        """
        # attempt to
        try:
            # find the channel's queue
            queue = self._queues[channel]
        # if it is not a subscriber
        except KeyError:
            # there is nothing to do
            return
        # if we are coalescing and this exact frame is already pending at the tail
        if coalesce and queue and queue[-1] == data:
            # there is no point queuing it twice
            return
        # if the queue is already full, this subscriber cannot keep up
        if len(queue) >= self._capacity:
            # drop it; its client will reconnect and pull fresh state
            self._drop(channel)
            # and there is nothing more to do
            return
        # otherwise, append the data
        queue.append(data)
        # and arm the channel for writing
        self._arm(channel)
        # all done
        return

    def flush(self, channel, **kwds):
        """
        The write-readiness handler: drain as much of {channel}'s queue as the socket accepts

        Returns {True} while bytes remain, so the dispatcher reschedules this handler, and
        {False} once the queue empties (or the connection breaks), so it is released.
        """
        # find the channel's queue
        queue = self._queues.get(channel)
        # if the channel is gone
        if queue is None:
            # forget it is armed
            self._armed.discard(channel)
            # and ask not to be rescheduled
            return False
        # while there are frames to deliver
        while queue:
            # peek at the head of the queue
            frame = queue[0]
            # attempt a partial, non-blocking send
            try:
                # hand as much as the socket will take
                sent = channel.send(frame)
            # if the socket buffer is full right now
            except BlockingIOError:
                # nothing went; try again when the socket is writable (this MUST come first, since
                # {BlockingIOError} is itself an {OSError})
                return True
            # if the connection is broken
            except OSError:
                # forget this subscriber now, rather than waiting for the read side to notice
                self.unsubscribe(channel)
                # and ask not to be rescheduled
                return False
            # if the socket did not take the whole frame
            if sent < len(frame):
                # put the unsent remainder back at the head
                queue[0] = frame[sent:]
                # and ask to be rescheduled when the socket is writable again
                return True
            # otherwise the frame is fully delivered; drop it
            queue.popleft()
        # the queue is empty; forget the channel is armed
        self._armed.discard(channel)
        # and release the write registration
        return False

    # meta-methods
    def __init__(
        self, dispatcher, capacity=1024, interval=None, keepalive=None, **kwds
    ):
        # chain up
        super().__init__(**kwds)
        # save the dispatcher, my source of write-readiness notifications and timers
        self.dispatcher = dispatcher
        # the most frames a single subscriber may have queued before it is dropped
        self._capacity = capacity
        # the keep-alive interval (a {pyre.units} time quantity) and the bytes to send each tick;
        # both must be set for the heartbeat to run
        self._interval = interval
        self._keepalive = keepalive
        # the topic -> set of subscribed channels map
        self._subscribers = collections.defaultdict(set)
        # the channel -> outbound byte queue map
        self._queues = {}
        # the set of channels currently registered for write-readiness
        self._armed = set()
        # whether the keep-alive timer is currently scheduled
        self._beating = False
        # all done
        return

    # implementation details
    def _arm(self, channel):
        """
        Register {channel} for write-readiness exactly once
        """
        # if the channel is already armed
        if channel in self._armed:
            # {whenWriteReady} appends a fresh handler on every call, so arming again would
            # pile a duplicate {flush} onto the same queue; do nothing
            return
        # mark it armed
        self._armed.add(channel)
        # and ask the dispatcher to call me back when the channel can accept bytes
        self.dispatcher.whenWriteReady(channel=channel, call=self.flush)
        # all done
        return

    def _drop(self, channel):
        """
        Forget and close a subscriber that has fallen too far behind to keep up
        """
        # remove it from my tables
        self.unsubscribe(channel)
        # and close its connection, so the client reconnects and pulls fresh state
        try:
            # let go of the socket
            channel.close()
        # if it is already gone
        except OSError:
            # there is nothing to do
            pass
        # all done
        return

    def _beat(self):
        """
        Make sure the keep-alive timer is scheduled, if a heartbeat is configured
        """
        # if a heartbeat is not configured, or one is already running
        if self._keepalive is None or self._interval is None or self._beating:
            # there is nothing to do
            return
        # mark the timer as running
        self._beating = True
        # and schedule the first tick; the handler reschedules itself by returning the interval
        self.dispatcher.alarm(interval=self._interval, call=self._heartbeat)
        # all done
        return

    def _heartbeat(self, timestamp):
        """
        Broadcast a keep-alive to every subscriber and ask to be rescheduled

        Returns the interval so the dispatcher fires this again; returns {None} when there are no
        subscribers left, which stops the timer until the next {subscribe} restarts it.
        """
        # if there is no one left to keep alive
        if not self._queues:
            # let the timer lapse
            self._beating = False
            # by declining to reschedule
            return None
        # otherwise, send the keep-alive to every subscriber; iterate a snapshot since a full
        # queue would drop its channel and mutate the map
        for channel in tuple(self._queues):
            # enqueue the keep-alive frame
            self.send(channel=channel, data=self._keepalive)
        # ask the dispatcher to fire this again after the same interval
        return self._interval

    # private data
    dispatcher = None
    _capacity = None
    _interval = None
    _keepalive = None
    _subscribers = None
    _queues = None
    _armed = None
    _beating = False


# end of file
