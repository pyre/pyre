# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
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


    # types
    from .exceptions import ConnectionResetError


    # behaviors
    @pyre.export(tip='register this service with the nexus')
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
        dispatcher.whenReadReady(channel=port, call=self.acknowledge)
        # all done
        return


    @pyre.export(tip='acknowledge a peer that has initiated a connection')
    def acknowledge(self, dispatcher, channel):
        """
        A peer has attempted to establish a connection
        """
        # accept the connection
        newChannel, peerAddress = channel.accept()
        # log the request
        self.info.log("{}: received 'connection' request from {}".format(channel, peerAddress))

        # if this is not a valid connection
        if not self.validate(channel=newChannel, address=peerAddress):
            # get rid of it
            newChannel.close()
            # and bail; indicate that i am interested in acknowledging other requests
            return True

        # process the connection; reschedule this handler to process more connection attempts
        # if {newPeer} returns {True}
        return self.connect(dispatcher=dispatcher, channel=newChannel, address=peerAddress)


    @pyre.export(tip='determine whether to start a conversation with the peer')
    def validate(self, channel, address):
        """
        Examine the peer {address} and determine whether to continue the conversation
        """
        # be friendly, by default
        return True


    @pyre.export(tip='indicate interest in continuing to interact with the peer')
    def connect(self, dispatcher, channel, address):
        """
        Prepare to start accepting requests from a new peer
        """
        # place the channel on the read list
        dispatcher.whenReadReady(channel=channel, call=self.respond)
        # indicate that i would like to continue receiving connection requests from other peers
        return True


    @pyre.export(tip='try to understand and respond to the peer request')
    def respond(self, dispatcher, channel):
        """
        Say something to the peer
        """
        # and prevent this from getting rescheduled; this is bad behavior because it can
        # potentially leave data in the channel, and it ignores the event raised when the peer
        # closes the connection
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
