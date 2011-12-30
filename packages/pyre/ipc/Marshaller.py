# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis, leif strand
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import pyre


# declaration
class Marshaller(pyre.interface, family="pyre.ipc.marshallers"):
    """
    Interface for components responsible for serializing python objects for transmission to
    other processes
    """


    # factory for my default implementation
    @classmethod
    def default(cls):
        from .Pickler import Pickler
        return Pickler


    # interface
    @pyre.provides
    def recv(self, channel):
        """
        Extract and return one object from {channel}
        """


    @pyre.provides
    def send(self, item, channel):
        """
        Pack and ship {item} over {channel}
        """


# end of file 
