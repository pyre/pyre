# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import pyre


# declaration
class Service(pyre.protocol, family="pyre.nexus.services"):
    """
    Protocol definition for components that handle network events
    """


    # default implementation
    @classmethod
    def pyre_default(cls, **kwds):
        """
        The suggested implementation of the {Service} protocol
        """
        # no opinions just yet
        return None


    # behaviors
    @pyre.provides
    def activate(self, nexus):
        """
        Register with the {nexus} and make it possible for me to start receiving information from
        the network
        """


    @pyre.provides(tip='acknowledge a peer that has initiated a connection')
    def acknowledge(self, dispatcher, channel):
        """
        A peer has attempted to establish a connection
        """


    @pyre.provides(tip='determine whether to start a conversation with the peer')
    def validate(self, channel, address):
        """
        Examine the peer {address} and determine whether to continue the conversation
        """


    @pyre.provides(tip='indicate interest in continuing to interact with the peer')
    def connect(self, dispatcher, channel, address):
        """
        Prepare to start accepting requests from a new peer
        """


    @pyre.provides(tip='try to understand and respond to the peer request')
    def process(self, dispatcher, channel):
        """
        Start or continue a conversation with a peer over {channel}
        """


# end of file
