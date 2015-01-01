# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis, leif strand
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import os
import pyre

from .Channel import Channel


# declaration
class Pipe(Channel):
    """
    A channel that uses pipes as the communication mechanism
    """


    # interface
    # life cycle management
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


    def close(self):
        """
        Shut down this channel
        """
        # close my descriptors
        os.close(self.infd)
        os.close(self.outfd)
        # and return
        return


    # access to the individual channel end points
    @property
    def inbound(self):
        """
        Retrieve the channel end point that can be read
        """
        # easy enough
        return self.infd


    @property
    def outbound(self):
        """
        Retrieve the channel end point that can be written
        """
        # easy enough
        return self.outfd


    # input/output
    def read(self, count):
        """
        Read {count} bytes from my input channel
        """
        # easy enough
        return os.read(self.infd, count)


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
