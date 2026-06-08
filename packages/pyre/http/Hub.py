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
    the server's event loop, riding the dispatcher's write-readiness notifications.
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

    def publish(self, event, topic=""):
        """
        Append the {event} bytes to the outbound queue of every subscriber to {topic}
        """
        # go through the subscribers of this topic
        for channel in self._subscribers.get(topic, ()):
            # and enqueue the event on each
            self.send(channel=channel, data=event)
        # all done
        return

    def send(self, channel, data):
        """
        Append the {data} bytes to {channel}'s outbound queue and arm it for delivery
        """
        # attempt to
        try:
            # find the channel's queue
            queue = self._queues[channel]
        # if it is not a subscriber
        except KeyError:
            # there is nothing to do
            return
        # append the data
        queue.append(data)
        # and arm the channel for writing
        self._arm(channel)
        # all done
        return

    def flush(self, channel, **kwds):
        """
        The write-readiness handler: drain as much of {channel}'s queue as the socket accepts

        Returns {True} while bytes remain, so the dispatcher reschedules this handler, and
        {False} once the queue empties, so the dispatcher releases the write registration.
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
            # attempt a partial, non-blocking send; a full send buffer raises {BlockingIOError}
            # and a broken connection raises {OSError}, both of which propagate to the
            # dispatcher, which reschedules or drops this handler accordingly
            sent = channel.send(frame)
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
    def __init__(self, dispatcher, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the dispatcher, my source of write-readiness notifications
        self.dispatcher = dispatcher
        # the topic -> set of subscribed channels map
        self._subscribers = collections.defaultdict(set)
        # the channel -> outbound byte queue map
        self._queues = {}
        # the set of channels currently registered for write-readiness
        self._armed = set()
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

    # private data
    dispatcher = None
    _subscribers = None
    _queues = None
    _armed = None


# end of file
