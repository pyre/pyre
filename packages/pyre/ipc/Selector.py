# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis, leif strand
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import pyre
import select
import collections
# my interface
from .protocols import dispatcher
# my base class
from .Scheduler import Scheduler


# declaration
class Selector(Scheduler, family='pyre.ipc.dispatchers.selector', implements=dispatcher):
    """
    An event demultiplexer implemented using the {select} system call.

    In addition to supporting alarms via its {Scheduler} base class, {Selector} monitors
    changes in the state of channels. Processes that hold {Selector} instances can go to sleep
    until either an alarm rings or a channel is ready for IO, at which point {Selector} invokes
    whatever handler is associated with the event.
    """


    # interface
    @pyre.export
    def notifyOnReadReady(self, channel, handler):
        """
        Add {handler} to the list of routines to call when {channel} is ready to be read
        """
        # add it to the pile
        self._read[channel.inbound].append(self._event(channel=channel, handler=handler))
        # and return
        return


    @pyre.export
    def notifyOnWriteReady(self, channel, handler):
        """
        Add {handler} to the list of routines to call when {channel} is ready to be written
        """
        # add it to the pile
        self._write[channel.outbound].append(self._event(channel=channel, handler=handler))
        # and return
        return


    @pyre.export
    def notifyOnException(self, channel, handler):
        """
        Add {handler} to the list of routines to call when something exceptional has happened
        to {channel}
        """
        # add both endpoints to the pile
        self._exception[channel.inbound].append(self._event(channel=channel, handler=handler))
        self._exception[channel.outbound].append(self._event(channel=channel, handler=handler))
        # and return
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
        # until someone says otherwise
        while self._watching:
            self._debug.line('watching:')
            # compute how long i am allowed to be asleep
            self._debug.line('    computing the allowed sleep interval')
            timeout = self.poll()
            self._debug.line('    max sleep: {}'.format(timeout))

            # construct the descriptor containers
            self._debug.line('    collecting the event sources')
            iwtd = self._read.keys()
            owtd = self._write.keys()
            ewtd = self._exception.keys()
            self._debug.line('      read: {}'.format(iwtd))
            self._debug.line('      write: {}'.format(owtd))
            self._debug.line('      exception: {}'.format(ewtd))

            # check for indefinite block
            self._debug.line('    checking for indefinite block')
            if not iwtd and not owtd and not ewtd and timeout is None:
                self._debug.log('** no registered handlers left; exiting')
                return

            # wait for an event
            try:
                self._debug.line('    calling select; timeout={!r}'.format(timeout))
                reads, writes, excepts = select.select(iwtd, owtd, ewtd, timeout)
            # when a signal is delivered to a handler registered by the application, the select
            # call is interrupted and raises a {select.error}
            except select.error as error:
                # unpack
                errno, msg = error.args
                # log
                self._debug.log('    signal received: errno={}: {}'.format(errno, msg))
                # keep going
                continue

            # dispatch to the handlers of file events
            self._debug.line('    dispatching to handlers')
            self.dispatch(self._exception, excepts)
            self.dispatch(self._write, writes)
            self.dispatch(self._read, reads)

            # raise the overdue alarms
            self._debug.log('    raising the alarms')
            self.awaken()
            
        # all done
        return


    def dispatch(self, index, entities):
        """
        Invoke the handlers registered in {index} that are associated with the descriptors in
        {entities}
        """
        # iterate over the active entities
        for active in entities:
            # invoke the event handlers and save the events whose handlers return {True}
            events = list(
                event for event in index[active] 
                if event.handler(selector=self, channel=event.channel)
                )
            # if no handlers requested to be rescheduled
            if not events:
                # remove the descriptor from the index
                del index[active]
            # otherwise
            else:
                # reschedule them
                index[active] = events
        # all done
        return


    # meta methods
    def __init__(self, **kwds):
        # delegate
        super().__init__(**kwds)

        # my file descriptor event indices
        self._read = collections.defaultdict(list)
        self._write = collections.defaultdict(list)
        self._exception = collections.defaultdict(list)

        # all done
        return


    # implementation details
    # private types
    class _event:
        """Encapsulate a channel and the associated call-back"""

        def __init__(self, channel, handler):
            self.channel = channel
            self.handler = handler
            return

        __slots__ = ('channel', 'handler')

    # private data
    _watching = True # controls whether to continue monitoring the event sources

    # my debug aspect
    import journal
    _debug = journal.debug('pyre.ipc.selector')
    del journal


# end of file 
