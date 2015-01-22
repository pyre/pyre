# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis, leif strand
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import pyre
# my protocol
from .Service import Service


# my declaration
class Server(pyre.component, implements=Service):
    """
    The base class for network servers
    """


    # user configurable state
    address = pyre.properties.inet()


    # behaviors
    @pyre.export
    def activate(self, nexus):
        """
        Register with the {nexus} and make it possible for me to start receiving information from
        the network
        """
        # build a port
        port = pyre.ipc.port(address=self.address)
        # get the nexus dispatcher
        dispatcher = nexus.dispatcher
        # ask it to monitor my port
        dispatcher.whenReadReady(channel=port, call=self.onConnectionAttempt)
        # all done
        return


    # implementation details
    def onConnectionAttempt(self, dispatcher, channel):
        """
        A peer has attempted to establish a connection
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
        return self.peer(dispatcher=dispatcher, channel=newChannel, address=peerAddress)


    def validateConnection(self, channel, address):
        """
        Examine the peer {address} and determine whether to continue the conversation
        """
        # be friendly, by default
        return True


    def peer(self, dispatcher, channel, address):
        """
        Prepare to start accepting requests from a new peer
        """
        # place the channel on the read list
        dispatcher.whenReadReady(channel=channel, call=self.respond)
        # indicate that i would like to continue receiving connection requests
        return True


    def respond(self, dispatcher, channel):
        """
        Say something to the peer
        """
        # be default, close the connection
        channel.close()
        # and prevent this from getting rescheduled
        return False


    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # build my log aspect
        import journal
        self.info = journal.info("pyre.nexus")
        # all done
        return

# end of file
