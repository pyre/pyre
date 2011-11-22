# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis, leif strand
# california institute of technology
# (c) 1998-2011 all rights reserved
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
