# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis, leif strand
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# externals
import os
import pyre

from .interfaces import channel


# declaration
class Pipe(pyre.component, family="pyre.ipc.channels.pipe", implements=channel):
    """
    A channel that uses pipes as the communication mechanism
    """


    # interface
    # life cycle management
    @pyre.export
    @classmethod
    def open(cls, **kwds):
        """
        Build a pair of pipes that are suitable for bidirectional communication between two
        processes
        """
        # build two matching pairs of file descriptors
        from_child, to_parent = os.pipe()
        from_parent, to_child = os.pipe()
        # dress them up as {Pipe} instances 
        parent = cls(infd=from_child, outfd=to_child, **kwds)
        child = cls(infd=from_parent, outfd=to_parent, **kwds)
        # and return them
        return parent, child


    @pyre.export
    def close(self):
        """
        Shut down this channel
        """
        # close my descriptors
        os.close(self.infd)
        os.close(self.outfd)
        # and return
        return


    # input/output
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
