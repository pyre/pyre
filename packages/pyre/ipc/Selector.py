# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import os
import pyre
import select
import collections
import weakref

# my interface
from . import dispatcher

# my base class
from .Scheduler import Scheduler

# the relay that delivers signals
from .Signals import Signals


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
        # interest in a channel that was forgotten revives it
        self._forgotten.discard(channel)
        # add it to the pile
        self._read[channel.inbound].append(self._event(channel=channel, handler=call, **kwds))
        # and return
        return

    @pyre.export
    def whenWriteReady(self, channel, call, **kwds):
        """
        Add {call} to the list of routines to call when {channel} is ready to be written
        """
        # interest in a channel that was forgotten revives it
        self._forgotten.discard(channel)
        # add it to the pile
        self._write[channel.outbound].append(self._event(channel=channel, handler=call, **kwds))
        # and return
        return

    @pyre.export
    def whenSignal(self, signal, call):
        """
        Add {call} to the list of routines to call from my event loop when the process receives
        {signal}
        """
        # hand it to the relay, which arranges for me to watch the channel it delivers on
        Signals.relay().watch(dispatcher=self, signal=signal, call=call)
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
    def forget(self, channel):
        """
        Stop watching {channel}: drop every handler registered on it, including the ones that
        are running right now, so a channel that is about to be closed leaves nothing behind
        under descriptor numbers that will be recycled
        """
        # the handlers that are running right now must not be put back when they are done
        self._forgotten.add(channel)
        # go through the endpoints of the channel
        for endpoint in {channel.inbound, channel.outbound}:
            # and drop its handlers from every pile
            self._read.pop(endpoint, None)
            self._write.pop(endpoint, None)
            self._exception.pop(endpoint, None)
        # all done
        return

    @pyre.export
    def channels(self):
        """
        Generate the set of channels currently being watched, each exactly once
        """
        # keep track of what has been reported
        seen = set()
        # go through my event tables, and the piles whose handlers are running right now
        for index in (self._read, self._write, self._exception, dict(enumerate(self._inflight))):
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
            # compute how long i am allowed to be asleep
            timeout = self.poll()
            # construct the descriptor containers
            iwtd = self._read.keys()
            owtd = self._write.keys()
            ewtd = self._exception.keys()

            # if anybody is listening
            if channel:
                # show them how long i may sleep
                channel.line("watching:")
                channel.line(f"    max sleep: {timeout}")
                # the input channels
                if iwtd:
                    channel.line(f"      read:")
                for fd in iwtd:
                    for event in self._read[fd]:
                        channel.line(f"        {event.channel}")
                # the output channels
                if owtd:
                    channel.line("      write:")
                for fd in owtd:
                    for event in self._write[fd]:
                        channel.line(f"        {event.channel}")
                # and the channels that are watching for exceptions
                if ewtd:
                    channel.line("      exception:")
                for fd in ewtd:
                    for event in self._exception[fd]:
                        channel.line(f"        {event.channel}")
                # flush
                channel.log()

            # the channel signals arrive on, if any; watching it is not a reason to stay up,
            # since a loop that is left with nothing but signals has run out of work
            relay = Signals.relay().channel()
            # so leave it out of the count
            sources = len(iwtd) - (relay in iwtd) + len(owtd) + len(ewtd)
            # if there is nothing to watch and no alarm to wait for
            if not sources and timeout is None:
                # if anybody is listening
                if channel:
                    # let them know why i am leaving
                    channel.log("** no registered handlers left; exiting")
                # and leave
                return

            # wait for an event; N.B.: a signal does not interrupt this, since the standard
            # library retries after running its handler (PEP 475), so a signal reaches the loop
            # only through the relay, as a read event
            try:
                reads, writes, excepts = select.select(iwtd, owtd, ewtd, timeout)
            # a registration whose descriptor died behind our back poisons the whole call
            except (OSError, ValueError):
                # find the corpses and drop them, so everybody else keeps getting served
                self._cull()
                # and try again
                continue

            # if anybody is listening
            if channel:
                # show them what woke me up
                channel.line("activity detected:")
                channel.line(f"      read clients: {len(reads)}")
                channel.line(f"      write clients: {len(writes)}")
                channel.line(f"      except clients: {len(excepts)}")
                # and the alarms that may be due
                channel.line(f"    raising alarms: {len(self._alarms)} registered")
                # flush
                channel.log()

            # dispatch to the handlers of file events
            self.dispatch(index=self._exception, entities=excepts)
            self.dispatch(index=self._write, entities=writes)
            self.dispatch(index=self._read, entities=reads)
            # raise the overdue alarms
            self.awaken()

        # if anybody is listening
        if channel:
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
            # the channels of the pile are still being watched while their handlers run,
            # so keep reporting them: a handler that forks, e.g. to form a team, must be
            # able to find the connection it is serving among the channels its child has
            # to release
            self._inflight.append(pile)
            # the events whose handlers ask to be rescheduled
            survivors = []
            # how many handlers have had their turn
            done = 0
            # carefully, since a handler that raises must not take the rest of the pile with
            # it: the ones that never got their turn are still interested, and losing them
            # leaves a channel nobody listens to, which is a silent failure
            try:
                # go through the handlers
                for event in pile:
                    # count this one before it runs, so that if it raises it is the one
                    # that is dropped
                    done += 1
                    # invoke it; a handler that returns {True} asks to be rescheduled
                    if event.handler(channel=event.channel, **event.context):
                        # so keep it
                        survivors.append(event)
            # whatever happened
            finally:
                # the pile is no longer in flight
                self._inflight.remove(pile)
                # the handlers that did not get their turn keep their place
                survivors += pile[done:]
                # unless their channel was forgotten while the pile was in flight
                survivors = [event for event in survivors if event.channel not in self._forgotten]
                # if anything is going back
                if survivors:
                    # put it back, ahead of whatever interest arrived while the handlers ran
                    index[active][:0] = survivors
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
        # the piles of events whose handlers are running
        self._inflight = []
        # the channels that were forgotten, whose running handlers must not be put back; they
        # are held weakly, so the record vanishes with the channel
        self._forgotten = weakref.WeakSet()

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
