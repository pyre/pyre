# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis, leif strand
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import pyre
import signal


# declaration
class Node(pyre.component):


    # public state
    port = None
    address = pyre.properties.inet() # just one, for now
    dispatcher = pyre.ipc.dispatcher()


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
        # if i already have a port, or i am not ready, bail
        if self.port or not now: return self.port
        # otherwise, build my port
        port = self.newPort()
        # register it with my dispatcher
        self.dispatcher.whenReadReady(channel=port, call=self.onConnectionAttempt)
        # and return it
        return port


    # high level event handlers
    def newPeer(self, channel, address):
        """
        Prepare to start accepting requests from a new peer
        """
        # place the channel on the read list
        self.dispatcher.whenReadReady(channel=channel, call=self.processRequest)
        # indicate that i would like to continue receiving connection requests
        return False


    def validateConnection(self, channel, address):
        """
        Examine the {address} of the connection requester and determine whether to keep talking to
        him or not
        """
        # be friendly, by default
        return True


    def shutdown(self):
        """
        Shut everything down and exit gracefully
        """
        # notify my dispatcher to exit its event loop
        self.dispatcher.stop()
        # all done
        return


    # low level event handlers
    def onConnectionAttempt(self, dispatcher, channel):
        """
        A peer has attempted to connect to my port
        """
        # accept the connection
        newChannel, peerAddress = channel.accept()
        # log the request
        self.info.log("{}: received 'connection' request from {}".format(channel, peerAddress))

        # if this is not a valid connection
        if not self.validateConnection(channel=newChannel, address=peerAddress):
            # show me
            self.info.log("  invalid connection; closing")
            # get rid of it
            newChannel.close()
            # and bail
            return True
        # process the connection; reschedule this handler to process more connection attempts
        # if {newPeer} returns {True}
        return self.newPeer(channel=newChannel, address=peerAddress)


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
        # register my signal handlers
        self.signals = self.registerSignalHandlers()
        # build my port
        self.port = self.activate(now=activate)
        # register it with my dispatcher
        self.dispatcher.whenReadReady(channel=self.port, call=self.onConnectionAttempt)

        # my debug aspect
        import journal
        self.info = journal.info("pyre.nexus")

        # all done
        return


    # implementation details
    def newPort(self):
        """
        Build and install a port that listens to my address for incoming connections
        """
        # make one
        port = pyre.ipc.port(address=self.address)
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



# end of file
