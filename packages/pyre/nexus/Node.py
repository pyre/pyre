# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
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
    dispatcher.doc = 'the component responsible for monitor my communication channels'

    services = pyre.properties.dict(schema=Service())
    services.doc = 'the table of available services'


    # interface
    @pyre.export
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


    @pyre.export
    def serve(self, plexus):
        """
        Start processing requests
        """
        # remember my application host
        self.plexus = plexus
        # enter the event loop of the dispatcher
        status = self.dispatcher.watch()
        # disconnect
        del self.plexus
        # status report
        return status


    @pyre.export
    def shutdown(self):
        """
        Shut everything down and exit gracefully
        """
        # notify my dispatcher to exit its event loop
        self.dispatcher.stop()
        # go through my services
        for name, service in self.services.items():
            # show me
            self.info.log('{}: shutting down {!r}'.format(self, name))
            # shut it down
            service.shutdown()
        # all done
        return


    # low level event handlers
    def reload(self, signal, frame):
        """
        Reload the nodal configuration for a distributed application
        """
        # log the request
        self.info.log("received 'reload' request")
        # NYI: what does 'reload' mean? does it involve the configuration store, or just the
        # layout of the distributed application?
        return


    def terminate(self, signal, frame):
        """
        Terminate the event processing loop
        """
        # log the request
        self.info.log("received 'terminate' request")
        # shut down
        self.shutdown()
        # and return
        return


    def signal(self, signal, frame):
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
            signal.SIGHUP: self.reload,
            signal.SIGINT: self.terminate,
            signal.SIGTERM: self.terminate,
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
            signal.signal(name, self.signal)
        # all done
        return signals


    # private data
    plexus = None


# end of file
