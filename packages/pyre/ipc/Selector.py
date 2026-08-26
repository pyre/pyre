# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import os
import pyre
import select
import collections

# my interface
from . import dispatcher

# my base class
from .Scheduler import Scheduler


# declaration
class Selector(Scheduler, family="pyre.ipc.dispatchers.selector", implements=dispatcher):
    """
    An event demultiplexer implemented using the {select} system call.

    In addition to supporting alarms via its {Scheduler} base class, {Selector} monitors
    changes in the state of channels. Processes that hold {Selector} instances can go to sleep
    until either an alarm rings or a channel is ready for IO, at which point {Selector} invokes
    whatever handler is associated with the event.
    """

    # interface
    @pyre.export
    def whenReadReady(self, channel, call, **kwds):
        """
        Add {call} to the list of routines to call when {channel} is ready to be read
        """
        # add it to the pile
        self._read[channel.inbound].append(self._event(channel=channel, handler=call, **kwds))
        # and return
        return

    @pyre.export
    def whenWriteReady(self, channel, call, **kwds):
        """
        Add {call} to the list of routines to call when {channel} is ready to be written
        """
        # add it to the pile
        self._write[channel.outbound].append(self._event(channel=channel, handler=call, **kwds))
        # and return
        return

    @pyre.export
    def whenException(self, channel, call, **kwds):
        """
        Add {call} to the list of routines to call when something exceptional has happened
        to {channel}
        """
        # add both endpoints to the pile
        self._exception[channel.inbound].append(self._event(channel=channel, handler=call, **kwds))
        self._exception[channel.outbound].append(self._event(channel=channel, handler=call, **kwds))
        # and return
        return

    @pyre.export
    def channels(self):
        """
        Generate the set of channels currently being watched, each exactly once
        """
        # keep track of what has been reported
        seen = set()
        # go through my event tables
        for index in (self._read, self._write, self._exception):
            # and the pile of events registered against each endpoint
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
        Request the selector to stop watching for further events
        """
        # adjust my state
        self._watching = False
        # and return
        return

    @pyre.export
    def watch(self):
        """
        Enter an indefinite loop of monitoring all registered event sources and invoking the
        registered event handlers
        """
        # reset my state
        self._watching = True
        # grab a channel
        channel = self._debug
        # until someone says otherwise
        while self._watching:
            # show me
            channel.line("watching:")
            # compute how long i am allowed to be asleep
            channel.line(f"    computing the allowed sleep interval")
            timeout = self.poll()
            channel.line(f"    max sleep: {timeout}")

            # construct the descriptor containers
            channel.line("    collecting the event sources")
            iwtd = self._read.keys()
            owtd = self._write.keys()
            ewtd = self._exception.keys()

            # if my channel is active
            if channel:
                # show me the input channels
                if iwtd:
                    channel.line(f"      read:")
                for fd in iwtd:
                    for event in self._read[fd]:
                        channel.line(f"        {event.channel}")
                # show me the output channels
                if owtd:
                    channel.line("      write:")
                for fd in owtd:
                    for event in self._write[fd]:
                        channel.line(f"        {event.channel}")
                # show me the channels that are watching for exceptions
                if ewtd:
                    channel.line("      exception:")
                for fd in ewtd:
                    for event in self._exception[fd]:
                        channel.line(f"        {event.channel}")

            # check for indefinite block
            channel.line("    checking for indefinite block")
            if not iwtd and not owtd and not ewtd and timeout is None:
                channel.log("** no registered handlers left; exiting")
                return

            # show me
            channel.log(f"    calling select; timeout={timeout}")
            # wait for an event
            try:
                reads, writes, excepts = select.select(iwtd, owtd, ewtd, timeout)
            # when a signal is delivered to a handler registered by the application, the select
            # call is interrupted and raises {InterruptedError}, a subclass of {OSError}
            except InterruptedError as error:
                # unpack
                errno = error.errno
                msg = error.strerror
                # show me
                channel.line(f"signal received: errno={errno}: {msg}")
                channel.line(f"  more watching: {self._watching}")
                channel.log()
                # keep going
                continue
            # a registration whose descriptor died behind our back poisons the whole call
            except (OSError, ValueError):
                # find the corpses and drop them, so everybody else keeps getting served
                self._cull()
                # and try again
                continue

            # if my channel is active
            if channel:
                # show me
                channel.line("activity detected:")
                # some details
                channel.line(f"      read clients: {len(reads)}")
                channel.line(f"      write clients: {len(writes)}")
                channel.line(f"      except clients: {len(excepts)}")
                # flush
                channel.log()

            # dispatch to the handlers of file events
            channel.log("    dispatching to handlers")
            self.dispatch(index=self._exception, entities=excepts)
            self.dispatch(index=self._write, entities=writes)
            self.dispatch(index=self._read, entities=reads)

            # raise the overdue alarms
            channel.log(f"    raising alarms: {len(self._alarms)} registered")
            self.awaken()

            # flush
            channel.log("moving on...")

        # sign off
        channel.log("done watching")
        # all done
        return

    def dispatch(self, index, entities):
        """
        Invoke the handlers registered in {index} that are associated with the descriptors in
        {entities}
        """
        # iterate over the active entities
        for active in entities:
            # take possession of the pile, so interest registered by the handlers while
            # they run accumulates separately instead of being invoked prematurely on
            # this pass
            pile = index.pop(active, [])
            # invoke the event handlers and save the events whose handlers return {True}
            events = list(
                event for event in pile if event.handler(channel=event.channel, **event.context)
            )
            # if any handlers requested to be rescheduled
            if events:
                # put them back, ahead of whatever interest arrived while they ran
                index[active][:0] = events
        # all done
        return

    def _cull(self):
        """
        Drop registrations whose descriptors are dead

        {select} refuses to scan a closed descriptor, so a single corpse would starve
        every healthy channel; this sweep runs when that happens and buries the corpses
        """
        # go through my event tables
        for index in (self._read, self._write, self._exception):
            # and a snapshot of their keys
            for key in list(index.keys()):
                # carefully
                try:
                    # resolve the key to a raw descriptor
                    fileno = key if isinstance(key, int) else key.fileno()
                    # closed high level objects report an invalid descriptor
                    if fileno < 0:
                        # which marks a corpse
                        raise ValueError(fileno)
                    # probe the descriptor
                    os.fstat(fileno)
                # if the resolution or the probe failed
                except (ValueError, OSError):
                    # this registration can never fire again
                    del index[key]
        # all done
        return

    # meta methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)

        # my file descriptor event indices
        self._read = collections.defaultdict(list)
        self._write = collections.defaultdict(list)
        self._exception = collections.defaultdict(list)

        # my debug aspect
        import journal

        self._debug = journal.debug("pyre.ipc.selector")

        # all done
        return

    # implementation details
    # private types
    class _event:
        """Encapsulate a channel and the associated call-back"""

        def __init__(self, channel, handler, **kwds):
            self.channel = channel
            self.handler = handler
            self.context = kwds
            return

        __slots__ = ("channel", "handler", "context")

    # private data
    _watching = True  # controls whether to continue monitoring the event sources


# end of file
