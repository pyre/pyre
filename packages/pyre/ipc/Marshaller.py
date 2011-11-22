# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# externals
import pyre


# declaration
class Marshaller(pyre.interface, family="pyre.ipc.marshallers"):
    """
    Interface for components responsible for serializing python objects for transmission to
    other processes
    """


    # interface
    @pyre.provides
    def recv(self, channel):
        """
        Extract and return one object from {channel}
        """


    @pyre.provides
    def send(self, channel, item):
        """
        Pack and ship {item} over {channel}
        """


# end of file 
