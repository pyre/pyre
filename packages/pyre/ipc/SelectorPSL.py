# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved

"""
A Dispatcher implementation that uses the default selector from the {selectors} module
in the python standard library
"""

# external
import errno
import selectors

# support
import pyre
import journal

# interface
from .Dispatcher import Dispatcher

# superclass
from .Scheduler import Scheduler


# declaration
class SelectorPSL(Scheduler, family="pyre.ipc.dispatchers.psl", implements=Dispatcher):
    """
    An event demultiplexer implemented using the high level interface in the {selectors} module of
    the python standard library

    The event piles are the single source of truth: the kernel side registration is derived
    from them whenever they change shape. This matters because descriptor numbers are recycled
    aggressively: a handler may close its channel and a fresh channel may reincarnate the same
    number within a single dispatch cycle, so no cached view of the kernel state can be trusted
    """

    # interface obligations
    @pyre.export
    def whenReadReady(self, channel, call, **kwds):
        """
        Add {call} to the handlers that will be invoked when {channel} is ready for reading
        """
        # get the read side of the channel
        fd = channel.inbound
        # a key with no registered interest is a fresh conversation, possibly on a recycled
        # descriptor number; its kernel registration must be rebuilt from scratch
        fresh = not self._read.get(fd) and not self._write.get(fd)
        # the interest that must be armed: whatever is already registered, plus reading
        mask = self._interest(key=fd) | selectors.EVENT_READ
        # arm the kernel side
        self._arm(key=fd, mask=mask, force=fresh)
        # and add the {event} to the read pile
        self._read.setdefault(fd, []).append(self._event(channel=channel, handler=call, **kwds))
        # all done
        return

    @pyre.export
    def whenWriteReady(self, channel, call, **kwds):
        """
        Add {call} to the handlers that will be invoked when {channel} is ready for writing
        """
        # get the write side of the channel
        fd = channel.outbound
        # a key with no registered interest is a fresh conversation, possibly on a recycled
        # descriptor number; its kernel registration must be rebuilt from scratch
        fresh = not self._read.get(fd) and not self._write.get(fd)
        # the interest that must be armed: whatever is already registered, plus writing
        mask = self._interest(key=fd) | selectors.EVENT_WRITE
        # arm the kernel side
        self._arm(key=fd, mask=mask, force=fresh)
        # and add the {event} to the write pile
        self._write.setdefault(fd, []).append(self._event(channel=channel, handler=call, **kwds))
        # all done
        return

    @pyre.export
    def whenException(self, channel, call):
        """
        Add {call} to the handlers that will be invoked when something exceptional happens to
        {channel}
        """
        # mark as unsupported, for now
        raise NotImplementedError(f"class '{type(self).__name__}' does not support 'whenException'")

    @pyre.export
    def channels(self):
        """
        Generate the set of channels currently being watched, each exactly once
        """
        # keep track of what has been reported
        seen = set()
        # go through my event tables
        for index in (self._read, self._write):
            # and the pile of events registered against each descriptor
            for events in index.values():
                # go through the events
                for event in events:
                    # get the channel
                    channel = event.channel
                    # if it has been reported already
                    if channel in seen:
                        # skip it
                        continue
                    # otherwise, mark it
                    seen.add(channel)
                    # and report it
                    yield channel
        # all done
        return

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
                # N.B.:
                #     a decision had to be made regarding the order that handlers are invoked
                #     this implementation calls the {read} handlers before the {write} handlers
                # if the {mask} indicates {fd} is ready for read
                if mask & selectors.EVENT_READ:
                    # invoke the read handlers
                    self.dispatch(index=read, key=fd)
                # if the {mask} indicates {fd} is ready for write
                if mask & selectors.EVENT_WRITE:
                    # invoke the write handlers
                    self.dispatch(index=write, key=fd)
                # settle this descriptor's kernel registration against the live piles, which
                # the handlers may have reshaped arbitrarily while they ran
                self._reconcile(key=fd)

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
        # take possession of the pile, so interest registered by the handlers while they run
        # accumulates separately instead of being invoked prematurely on this pass
        pile = index.pop(key, [])
        # make a pile of event handlers to reschedule
        reschedule = []
        # how many handlers have had their turn
        done = 0
        # carefully, since a handler that raises something other than an {OSError} must not
        # take the rest of the pile with it: the ones that never got their turn are still
        # interested, and losing them leaves a channel nobody listens to
        try:
            # go through the snapshot
            for event in pile:
                # count this one before it runs, so that if it raises it is the one that is
                # dropped
                done += 1
                # very very carefully
                try:
                    # invoke the handler
                    keep = event.handler(channel=event.channel, **event.context)
                # if a transient error occurs
                except (BlockingIOError, InterruptedError):
                    # let's try this again
                    keep = True
                # if something more serious happens
                except OSError as error:
                    # discarding the handler is the only sane move, but say so, since a
                    # silent drop is undiagnosable: a broken connection is routine and goes
                    # on the debug channel, while a process that has run out of resources,
                    # e.g. file descriptors, is news that must reach somebody
                    exhausted = error.errno in (errno.EMFILE, errno.ENFILE, errno.ENOMEM)
                    # pick the channel accordingly
                    channel = (
                        journal.warning("pyre.ipc.psl")
                        if exhausted
                        else journal.debug("pyre.ipc.psl")
                    )
                    # describe what happened
                    channel.line(f"discarding a handler of {event.channel}")
                    channel.line(f"after it raised {error}")
                    # flush
                    channel.log()
                    # and drop it
                    keep = False
                # keepers
                if keep:
                    # get rescheduled
                    reschedule.append(event)
        # whatever happened
        finally:
            # the handlers that did not get their turn keep their place
            reschedule += pile[done:]
            # if any handlers survived
            if reschedule:
                # put them back, ahead of whatever interest arrived while they ran
                index.setdefault(key, [])[:0] = reschedule
        # all done
        return

    def _interest(self, key):
        """
        Compute the event mask implied by the current piles of {key}
        """
        # reading, if there are read handlers; writing, if there are write handlers
        return (selectors.EVENT_READ if self._read.get(key) else 0) | (
            selectors.EVENT_WRITE if self._write.get(key) else 0
        )

    def _arm(self, key, mask, force=False):
        """
        Ensure the kernel watches {key} for {mask}

        With {force}, any standing registration under this descriptor number is torn down
        first: the caller knows the conversation is fresh, so an existing entry is a leftover
        from a closed channel that recycled the number, and the kernel side filter it claims
        to hold died with the original descriptor
        """
        # get my selector
        selector = self._selector
        # carefully
        try:
            # look up the standing registration under this descriptor number
            current = self._selector.get_key(key)
        # if there is none
        except KeyError:
            # so note
            current = None
        # a standing registration can be trusted only when nobody demands a rebuild, it
        # belongs to this very endpoint, and it watches for exactly the right events; the
        # ownership test is meaningful only for object endpoints, since a raw descriptor
        # number cannot be told apart from its own reincarnation
        if (
            current is not None
            and not force
            and (isinstance(key, int) or current.fileobj is key)
            and current.events == mask
        ):
            # nothing to do
            return
        # if there is a standing registration
        if current is not None:
            # carefully, since its descriptor may be long dead
            try:
                # tear it down
                selector.unregister(key)
            # tolerating whatever state it is in
            except (KeyError, ValueError, OSError):
                # nothing further
                pass
        # and register afresh; a dead endpoint raises out of here, for the caller to judge
        selector.register(key, events=mask)
        # all done
        return

    def _reconcile(self, key):
        """
        Settle the kernel registration of {key} against the live piles
        """
        # compute the interest implied by the piles
        mask = self._interest(key=key)
        # if nothing is left
        if not mask:
            # carefully, since the descriptor may already be gone
            try:
                # tear down the registration
                self._selector.unregister(key)
            # tolerating whatever state it is in
            except (KeyError, ValueError, OSError):
                # nothing further
                pass
            # all done
            return
        # otherwise, carefully
        try:
            # make sure the kernel watches for exactly this interest
            self._arm(key=key, mask=mask)
        # if the endpoint is dead
        except (ValueError, OSError):
            # its handlers can never fire again; drop them
            self._read.pop(key, None)
            self._write.pop(key, None)
        # all done
        return

    # implementation details - private types
    class _event:
        """
        Pair a channel with a callback
        """

        # metamethods
        def __init__(self, channel, handler, **kwds):
            # store
            self.channel = channel
            self.handler = handler
            self.context = kwds
            # all done
            return

        # trim
        __slots__ = "channel", "handler", "context"


# end of file
