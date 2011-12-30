# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis, leif strand
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import pyre
import journal
from . import interfaces


# declaration
class Node(pyre.component):


    # public state
    marshaller = pyre.facility(interface=interfaces.marshaller)
    dispatcher = pyre.facility(interface=interfaces.dispatcher)


    # interface
    # signal handling
    def registerSignalHandlers(self):
        """
        By default, nodes register handlers for process termination and configuration reload.
        """
        # get the {signal} package
        import signal
        # register the two basic handlers
        signal.signal(signal.SIGHUP, self.onReload)
        signal.signal(signal.SIGTERM, self.onTerminate)
        # all done
        return


    def onReload(self, *unused):
        """
        Reload the nodal configuration for a distributed application
        """
        # log the request
        self.info.log("received 'reload' request")
        # NYI: what does 'reload' mean? does it involve the configuration store, or just the
        # layout of the distributed application?
        return


    def onTerminate(self, *unused):
        """
        Terminate the event processing loop
        """
        # log the request
        self.info.log("received 'terminate' request")
        # notify my dispatcher to exit its event loop
        self.dispatcher.stop()
        # and return
        return


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)

        # register my signal handlers
        self.registerSignalHandlers()

        # all done
        return


    # private data
    info = journal.info("pyre.ipc.nodes")


# end of file 
