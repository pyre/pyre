# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# externals
import pyre


# declaration
class Nexus(pyre.protocol, family="pyre.nexus.servers"):
    """
    Protocol definition for components that enable applications to interact over the network
    """


    #  obligations
    @pyre.provides
    def activate(self, application, **kwds):
        """
        Prepare to receive events by pairing services with communication channels
        """

    @pyre.provides
    def serve(self, plexus, **kwds):
        """
        Wait for events in registered channels and dispatch them to associated services
        """

    @pyre.provides
    def shutdown(self):
        """
        Shut down the event loop
        """


    # default implementation
    @classmethod
    def pyre_default(cls, **kwds):
        """
        The default implementation of the {Nexus} protocol
        """
        # get my favorite
        from .Node import Node
        # return it
        return Node


# end of file
