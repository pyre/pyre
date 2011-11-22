# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# externals
import os
import pyre

from .Channel import Channel


# declaration
class Pipe(pyre.component, family="pyre.ipc.channels.pipe", implements=Channel):
    """
    A channel that uses pipes as the communication mechanism
    """


    # interface
    @classmethod
    def open(cls):
        """
        Build a pair of pipes that are suitable for bidirectional communication between two
        processes
        """
        # build two matching pairs of file descriptors
        from_child, to_parent = os.pipe()
        from_parent, to_child = os.pipe()
        # dress them up as {Pipe} instances 
        parent = cls(infd=from_child, outfd=to_child)
        child = cls(infd=from_parent, outfd=to_parent)
        # and return them
        return parent, child


    @pyre.export
    def read(self, count):
        """
        Read {count} bytes from my input channel
        """
        # easy enough
        return os.read(self.infd, count)


    @pyre.export
    def write(self, bstr):
        """
        Write the bytes in {bstr} to my output channel
        """
        # easy enough
        return os.write(self.outfd, bstr)


    # meta methods
    def __init__(self, infd, outfd, **kwds):
        super().__init__(**kwds)
        self.infd = infd
        self.outfd = outfd
        return


    # private data
    infd = None
    outfd = None
        
    

# end of file 
