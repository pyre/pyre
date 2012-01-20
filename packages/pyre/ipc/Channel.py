# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis, leif strand
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import pyre


# declaration
class Channel(pyre.interface, family="pyre.ipc.channels"):
    """
    A wrapper around the lower level IPC mechanisms that normalizes the sending and receiving
    of messages. See {Pipe} and {Socket} for concrete examples of encapsulation of the
    operating system services.
    """ 


    # interface
    # channel life cycle management
    @pyre.provides
    @classmethod
    def open(cls, **kwds):
        """
        Channel factory
        """


    @pyre.provides
    def close(self):
        """
        Shutdown the channel
        """

    # access to the individual channel end points
    @pyre.provides
    @property
    def inbound(self):
        """
        Retrieve the channel end point that can be read
        """

    @pyre.provides
    @property
    def outbound(self):
        """
        Retrieve the channel end point that can be written
        """

    # input/output
    @pyre.provides
    def read(self, count):
        """
        Read {count} bytes from my input channel
        """


    @pyre.provides
    def write(self, bstr):
        """
        Write the bytes in {bstr} to output channel
        """


# end of file 
