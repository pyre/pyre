# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved

"""
A Dispatcher implementation that uses the default selector from the {selectors} module
in the python standard library
"""


# external
import pyre
import journal
import collections
import selectors

# interface
from .Dispatcher import Dispatcher

# superclass
from .Scheduler import Scheduler


# declaration
class SelectorPSL(Scheduler, family="pyre.ipc.dispatchers.psl", implements=Dispatcher):
    """
    An event demultiplexer implemented using the high level interface in the {selectors} module of
    the python standard library
    """

    # interface obligations
    @pyre.export
    def whenReadReady(self, channel, call):
        """
        Add {call} to the handlers that will be invoked when {channel} is ready for reading
        """
        # get my selector
        selector = self._selector
        # get the read side of the channel
        fd = channel.inbound
        # bind the {channel} with the {call} handler
        event = self._event(channel=channel, handler=call)
        # get the current event mask
        current = self._masks[fd]
        # turn on the read bit
        updated = current | selectors.EVENT_READ
        # if the mask is modified
        if current != updated:
            # store the updated mask
            self._masks[fd] = updated
            # if the file descriptor is not already registered
            try:
                # add it to the watch list
                selector.register(fd, events=updated)
            # if it's already registered
            except KeyError:
                # modify the registration
                selector.modify(fileobj=fd, events=updated)
        # in any case, add the {event} to the read pile
        self._read.setdefault(fd, []).append(event)
        # all done
        return

    @pyre.export
    def whenWriteReady(self, channel, call):
        """
        Add {call} to the handlers that will be invoked when {channel} is ready for writing
        """
        # get my selector
        selector = self._selector
        # get the read side of the channel
        fd = channel.outbound
        # bind the {channel} with the {call} handler
        event = self._event(channel=channel, handler=call)
        # get the current event mask
        current = self._masks[fd]
        # turn on the read bit
        updated = current | selectors.EVENT_WRITE
        # if the mask is modified
        if current != updated:
            # store the updated mask
            self._masks[fd] = updated
            # if the file descriptor is not already registered
            try:
                # add it to the watch list
                selector.register(fd, events=updated)
            # if it's already registered
            except KeyError:
                # modify the registration
                selector.modify(fileobj=fd, events=updated)
        # in any case, add the {event} to the read pile
        self._write.setdefault(fd, []).append(event)
        # all done
        return

    @pyre.export
    def whenException(self, channel, call):
        """
        Add {call} to the handlers that will be invoked when something exceptional happens to
        {channel}
        """
        # mark as unsupported, for now
        raise NotImplementedError(
            f"class '{type(self).__name__}' does not support 'whenException'"
        )

    @pyre.export
    def stop(self):
        """
        Ask the selector to stop waiting for further events
        """
        # update my state
        self._watching = False
        # and return
        return

    @pyre.export
    def watch(self):
        """
        Start monitoring the registered event sources
        """
        # get my selector
        selector = self._selector
        # my registration tables
        read = self._read
        write = self._write
        # and the table of event masks
        masks = self._masks
        # reset my state
        self._watching = True

        # until someone says otherwise
        while self._watching:
            # compute how long i'm allowed to sleep before an alarm triggers
            # N.B.: {poll} returns {None} when no alarms are registered
            timeout = self.poll()
            # if there is nothing to watch
            if not (read or write) and timeout is None:
                # mark
                self._watching = False
                # and bail
                break
            # otherwise, carefully
            try:
                # wait for something interesting to happen
                selection = selector.select(timeout=timeout)
            # if we have a runaway signal
            except InterruptedError:
                # make a trivial selection so the loop continues
                selection = ()
            # go through the response
            for key, mask in selection:
                # get the corresponding file descriptor
                fd = key.fileobj
                # and the events we are watching
                event = masks[fd]
                # N.B.:
                #     a decision had to be made regarding the order that handlers are invoked
                #     this implementation calls the {read} handlers before the {write} handlers
                # if the {mask} indicates {fd} is ready for read
                if mask & selectors.EVENT_READ:
                    # invoke the write handlers
                    reschedule = self.dispatch(index=read, key=fd)
                    # if there is something to reschedule
                    if reschedule:
                        # update the {write} map
                        read[fd] = reschedule
                    # otherwise
                    else:
                        # remove this file descriptor from the pile
                        read.pop(fd, 0)
                        # clear the {write} bit from its mask
                        event &= ~selectors.EVENT_READ
                # if the {mask} indicates {fd} is ready for write
                if mask & selectors.EVENT_WRITE:
                    # invoke the write handlers
                    reschedule = self.dispatch(index=write, key=fd)
                    # if there is something to reschedule
                    if reschedule:
                        # update the {write} map
                        write[fd] = reschedule
                    # otherwise
                    else:
                        # remove this file descriptor from the pile
                        write.pop(fd, 0)
                        # clear the {write} bit from its mask
                        event &= ~selectors.EVENT_WRITE
                # if the {event} mask of this {fd} is now trivial
                if event == 0:
                    # unregister it
                    selector.unregister(fileobj=fd)
                    # and remove it from the mask table
                    masks.pop(fd, 0)
                # otherwise
                else:
                    # if the event has been modified
                    if masks[fd] != event:
                        # modify the selector registration
                        selector.modify(fileobj=fd, events=event)
                        # and update the table
                        masks[fd] = event

            # raise any overdue alarms
            self.awaken()

        # all done
        return

    # metamethods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # instantiate the default selector
        self._selector = selectors.DefaultSelector()
        # set up my termination flag
        self._watching = False

        # set up the event mask map: fd -> mask
        self._masks = collections.defaultdict(int)
        # set up the read map: fd -> list[_event]
        self._read = {}
        # and the write map: fd -> list[_event]
        self._write = {}

        # all done
        return

    # implementation details - methods
    def dispatch(self, index, key):
        """
        Invoke the handlers for {key} registered in {index}
        """
        # make a pile of event handlers to reschedule
        reschedule = []
        # go through the pile registered under {key}
        for event in index.get(key, ()):
            # very very carefully
            try:
                # invoke the handler
                keep = event.handler(channel=event.channel)
            # if a transient error occurs
            except (BlockingIOError, InterruptedError):
                # let's try this again
                keep = True
            # if something more serious happens
            except OSError:
                # something is wrong with the connection; discard the handler
                keep = False
            # keepers
            if keep:
                # get rescheduled
                reschedule.append(event)
        # hand off the rescheduling pile
        return reschedule

    # implementation details - private types
    class _event:
        """
        Pair a channel with a callback
        """

        # metamethods
        def __init__(self, channel, handler):
            # store
            self.channel = channel
            self.handler = handler
            # all done
            return

        # trim
        __slots__ = "channel", "handler"


# end of file
