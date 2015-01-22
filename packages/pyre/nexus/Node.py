# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis, leif strand
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import pyre
import signal
# my protocols
from .Nexus import Nexus
from .Service import Service


# declaration
class Node(pyre.component, family="pyre.nexus.servers.node", implements=Nexus):


    # user configurable state
    dispatcher = pyre.ipc.dispatcher()
    services = pyre.properties.dict(schema=Service())


    # interface
    def serve(self):
        """
        Start processing requests
        """
        # easy: delegate to my dispatcher
        return self.dispatcher.watch()


    def activate(self, now=True):
        """
        Get ready to listen for incoming connections

        This can be done at construction time by passing {activate=True}
        """
        # go through my services
        for name, service in self.services.items():
            # show me
            self.info.log('{}: activating {!r}'.format(self, name))
            # activate it
            service.activate(nexus=self)
        # all done
        return


    # high level event handlers
    def shutdown(self):
        """
        Shut everything down and exit gracefully
        """
        # notify my dispatcher to exit its event loop
        self.dispatcher.stop()
        # all done
        return


    # low level event handlers
    def onReload(self, signal, frame):
        """
        Reload the nodal configuration for a distributed application
        """
        # log the request
        self.info.log("received 'reload' request")
        # NYI: what does 'reload' mean? does it involve the configuration store, or just the
        # layout of the distributed application?
        return


    def onTerminate(self, signal, frame):
        """
        Terminate the event processing loop
        """
        # log the request
        self.info.log("received 'terminate' request")
        # shut down
        self.shutdown()
        # and return
        return


    def onSignal(self, signal, frame):
        """
        Dispatch {signal} to the registered handler
        """
        # log the request
        self.info.log("received signal {}".format(signal))
        # locate the handler
        handler = self.signals[signal]
        # and invoke it
        return handler(signal=signal, frame=frame)


    # meta methods
    def __init__(self, activate=True, **kwds):
        # chain up
        super().__init__(**kwds)

        # my debug aspect
        import journal
        self.info = journal.info("pyre.nexus")

        # register my signal handlers
        self.signals = self.registerSignalHandlers()
        # activate my services
        self.activate(now=activate)

        # all done
        return


    # implementation details
    # signal handling
    def newSignalIndex(self):
        """
        By default, nodes register handlers for process termination and configuration reload
        """
        # build my signal index
        signals = {
            signal.SIGHUP: self.onReload,
            signal.SIGINT: self.onTerminate,
            signal.SIGTERM: self.onTerminate,
            }
        # and return it
        return signals


    def registerSignalHandlers(self):
        """
        By default, nodes register handlers for process termination and configuration reload
        """
        # build my signal index
        signals = self.newSignalIndex()
        # register the signal demultiplexer
        for name in signals.keys():
            # register the three basic handlers
            signal.signal(name, self.onSignal)
        # all done
        return signals


# end of file
