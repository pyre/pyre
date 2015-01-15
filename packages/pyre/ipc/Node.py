# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis, leif strand
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import pyre
import journal
import signal
# my protocols
from . import protocols


# declaration
class Node(pyre.component):


    # public state
    address = pyre.properties.inet() # just one, for now
    marshaller = protocols.marshaller()
    dispatcher = protocols.dispatcher()


    # interface
    def serve(self):
        """
        Start processing requests
        """
        # easy: delegate to my dispatcher
        return self.dispatcher.watch()


    # event handlers
    def onConnectionAttempt(self, selector=None, channel=None):
        """
        A peer has attempted to connect to my port
        """
        # log the request
        self.info.log("received 'connection' request from {}".format(channel.address))
        # reschedule this handler
        return True


    def onReload(self, selector=None, channel=None, signal=None, frame=None):
        """
        Reload the nodal configuration for a distributed application
        """
        # log the request
        self.info.log("received 'reload' request")
        # NYI: what does 'reload' mean? does it involve the configuration store, or just the
        # layout of the distributed application?
        return


    def onTerminate(self, selector=None, channel=None, signal=None, frame=None):
        """
        Terminate the event processing loop
        """
        # log the request
        self.info.log("received 'terminate' request")
        # notify my dispatcher to exit its event loop
        self.dispatcher.stop()
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
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # register my signal handlers
        self.signals = self.registerSignalHandlers()
        # build my port
        self.port = self.newPort()
        # register it with my dispatcher
        self.dispatcher.notifyOnReadReady(channel=self.port, handler=self.onConnectionAttempt)
        # all done
        return


    # implementation details
    def newPort(self):
        """
        Build and install a port that listens to my address for incoming connections
        """
        # access the port factory
        from .PortTCP import PortTCP
        # make one
        port = PortTCP.install(address=self.address)
        # and return it
        return port


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


    # private data
    info = journal.info("pyre.ipc.nodes")


# end of file
