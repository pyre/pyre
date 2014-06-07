# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis, leif strand
# orthologue
# (c) 1998-2014 all rights reserved
#


# externals
import pyre
import journal
# my protocols
from . import protocols


# declaration
class Node(pyre.component):


    # public state
    address = pyre.properties.inet() # just one, for now
    marshaller = protocols.marshaller()
    dispatcher = protocols.dispatcher()


    # interface
    # signal handling
    def registerSignalHandlers(self):
        """
        By default, nodes register handlers for process termination and configuration reload
        """
        # get the {signal} package
        import signal
        # register the two basic handlers
        signal.signal(signal.SIGHUP, self.onReload)
        signal.signal(signal.SIGTERM, self.onTerminate)
        # all done
        return


    def onReload(self, *uargs, **ukwds):
        """
        Reload the nodal configuration for a distributed application
        """
        # log the request
        self.info.log("received 'reload' request")
        # NYI: what does 'reload' mean? does it involve the configuration store, or just the
        # layout of the distributed application?
        return


    def onTerminate(self, *uargs, **ukwds):
        """
        Terminate the event processing loop
        """
        # log the request
        self.info.log("received 'terminate' request")
        # notify my dispatcher to exit its event loop
        self.dispatcher.stop()
        # and return
        return


    def onConnectionAttempt(self, channel, **kwds):
        """
        A peer has attempted to connect to my port
        """
        # log the request
        self.info.log("received 'connection' request from {}".format(channel.address))
        # reschedule this handler
        return True


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)

        # register my signal handlers
        self.registerSignalHandlers()

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


    # private data
    info = journal.info("pyre.ipc.nodes")


# end of file 
