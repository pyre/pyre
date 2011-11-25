# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# externals
import select
import collections
# my base class
from .Scheduler import Scheduler


# declaration
class Selector(Scheduler):
    """
    The manager of a set of file descriptors and the registered handlers for the events they
    generate. File descriptors can generate read, write and exception events that correspond to
    changes in their state. Processes that hold instances of {Selector} call {watch} to enter
    an idle state until some event wakes up the process and its handler is invoked.
    """


    # interface
    def notifyOnReadReady(self, fd, handler):
        """
        Add {handler} to the list of routines to call when {fd} is ready to be read
        """
        # add it to the pile
        self._input[fd].append(handler)
        # and return


    def notifyOnWriteReady(self, fd, handler):
        """
        Add {handler} to the list of routines to call when {fd} is ready to be written
        """
        # add it to the pile
        self._output[fd].append(handler)
        # and return


    def notifyOnException(self, fd, handler):
        """
        Add {handler} to the list of routines to call when something exceptional has happened
        to {fd}
        """
        # add it to the pile
        self._exception[fd].append(handler)
        # and return


    def watch(self):
        """
        Enter an indefinite loop of monitoring all registered event sources and invoking the
        registered event handlers
        """
        # reset my state
        self._watching = True
        # until someone says otherwise
        while self._watching:
            self._debug.line("watching:")
            # compute how long i am allowed to be asleep
            self._debug.line("    computing the allowed sleep interval")
            timeout = self.poll()

            # construct the descriptor containers
            self._debug.line("    collecting the event sources")
            iwtd = self._input.keys()
            owtd = self._output.keys()
            ewtd = self._exception.keys()
            self._debug.line("      input: {}".format(iwtd))
            self._debug.line("      output: {}".format(owtd))
            self._debug.line("      exception: {}".format(ewtd))

            # check for indefinite block
            self._debug.line("    checking for indefinite block")
            if not iwtd and not owtd and not ewtd and timeout is None:
                self._debug.log("** no registered handlers left; exiting")
                return

            # wait for an event
            try:
                self._debug.line("    calling select; timeout={!r}".format(timeout))
                reads, writes, excepts = select.select(iwtd, owtd, ewtd, timeout)
            # when a signal is delivered to a handler registered by the application, the select
            # call is interrupted and raises a {select.error}
            except select.error as error:
                # unpack
                errno, msg = error.args
                # log
                self._debug.log("    signal received: errno={}: {}".format(errno, msg))
                # keep going
                continue

            # dispatch to the handlers of file events
            self._debug.line("    dispatching to handlers")
            self.dispatch(self._exception, excepts)
            self.dispatch(self._output, writes)
            self.dispatch(self._input, reads)

            # raise the overdue alarms
            self._debug.log("    raising the alarms")
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
            # invoke the handlers and save the ones that return {True}
            handlers = list(
                handler for handler in index[active] if handler(selector=self, descriptor=active))
            # if no handlers requested to be rescheduled
            if not handlers:
                # remove the descriptor from the index
                del index[active]
            # otherwise
            else:
                index[active] = handlers
        # all done
        return


    def stop(self):
        """
        Request the selector to stop watching for further events
        """
        # adjust my state
        self._watching = False
        # and return
        return


    # meta methods
    def __init__(self, **kwds):
        # delegate
        super().__init__(**kwds)

        # my file descriptor event indices
        self._input = collections.defaultdict(list)
        self._output = collections.defaultdict(list)
        self._exception = collections.defaultdict(list)

        # all done
        return


    # private data
    _watching = True # controls whether to continue monitoring the event sources
    # my debug aspect
    import journal
    _debug = journal.debug("pyre.ipc.selector")
    del journal


# end of file 
