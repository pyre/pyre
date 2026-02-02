# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# leif strand
# (c) 1998-2026 all rights reserved


# externals
import os

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
    def read(self, minlen: int = 0, maxlen: int = 64 * 1024):
        """
        Read {count} bytes from my input channel
        """
        # make sure
        if maxlen < minlen:
            # that the limits are sane
            maxlen = minlen
        # reset the byte count
        total = 0
        # initialize the packet pile
        packets = []
        # for as long as it takes
        while True:
            # pull something from the channel
            packet = os.read(self.infd, maxlen - total)
            # get its length
            got = len(packet)
            # if we got nothing, the channel is closed; bail
            if got == 0:
                break
            # otherwise, update the total
            total += got
            # and save the packet
            packets.append(packet)
            # if we have reached our goal
            if total >= minlen:
                # bail
                break
        # assemble the byte string and return it
        return b"".join(packets)

    def write(self, bytes: bytes):
        """
        Write the {bytes} to my output channel
        """
        # easy enough
        return os.write(self.outfd, bytes)

    # meta methods
    def __init__(self, infd: int, outfd: int, **kwds):
        # chain up
        super().__init__(**kwds)
        # and my file descriptors
        self.infd = infd
        self.outfd = outfd
        return

    def __str__(self):
        # build a human readable representation
        return f"pipe in={self.infd}, out={self.outfd}"


# end of file
