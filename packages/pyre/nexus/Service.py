# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis, leif strand
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


# end of file
