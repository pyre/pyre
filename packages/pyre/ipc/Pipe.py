# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import os

# my superclass
from .Channel import Channel

# the exception raised when asked to carry descriptors
from .exceptions import CarriageError


# declaration
class Pipe(Channel):
    """
    A channel that uses pipes as the communication mechanism

    A pipe channel reads from one pipe and writes to another; either may be missing, which
    makes a channel that only reads or only writes
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
        # one for each direction
        from_parent, to_child = os.pipe()
        # make sure the parent side file descriptors are not inherited by any process created by
        # the {exec} family of spawners
        cls.setCLOEXEC(to_child)
        # both of them
        cls.setCLOEXEC(from_child)
        # similarly, mark the child endpoints as inheritable
        cls.clearCLOEXEC(to_parent)
        # both of them
        cls.clearCLOEXEC(from_parent)
        # dress up the end points as {Pipe} instances
        parent = cls(infd=from_child, outfd=to_child, **kwds)
        # on both sides
        child = cls(infd=from_parent, outfd=to_parent, **kwds)
        # and return them as a labeled pair, so the order is part of the contract
        return cls.ends(parent=parent, child=child)

    def close(self):
        """
        Shut down this channel
        """
        # close my descriptors
        for descriptor in self.descriptors():
            # one at a time
            os.close(descriptor)
        # and return
        return

    # access to the individual channel end points
    @property
    def inbound(self):
        """
        Retrieve the descriptor of the channel end point that can be read
        """
        # easy enough
        return self.infd

    @property
    def outbound(self):
        """
        Retrieve the descriptor of the channel end point that can be written
        """
        # easy enough
        return self.outfd

    def descriptors(self):
        """
        The descriptors i am made of: the end i read from, then the end i write to, whichever i
        have
        """
        # easy enough
        return [descriptor for descriptor in (self.infd, self.outfd) if descriptor is not None]

    # input/output
    def read(self, minlen: int = 0, maxlen: int = 64 * 1024):
        """
        Read at least {minlen} and at most {maxlen} bytes from my input channel, or whatever
        arrives before it closes
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
            # if we got nothing, the channel is closed
            if got == 0:
                # bail
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

    def write(self, bytes: bytes, descriptors=()):
        """
        Write the {bytes} to my output channel; pipes cannot carry open {descriptors}
        """
        # if i am asked to carry descriptors
        if descriptors:
            # refuse
            raise CarriageError(channel=self, reason="pipes carry bytes only")
        # otherwise, write
        return os.write(self.outfd, bytes)

    # travel
    def hints(self):
        """
        Record which of my ends i have, so my descriptors can be told apart on arrival
        """
        # name the ends that are present
        ends = [name for name, end in (("in", self.infd), ("out", self.outfd)) if end is not None]
        # and hand them off
        return {"ends": ",".join(ends)}

    @classmethod
    def rebuild(cls, hints, descriptors):
        """
        Build a pipe channel from its {hints} and its {descriptors}
        """
        # match the descriptors with the ends they belong to
        ends = dict(zip(hints["ends"].split(","), descriptors))
        # and build the channel
        return cls(infd=ends.get("in"), outfd=ends.get("out"))

    # meta methods
    def __init__(self, infd: int | None = None, outfd: int | None = None, **kwds):
        # chain up
        super().__init__(**kwds)
        # the end i read from, if any
        self.infd = infd
        # and the end i write to, if any
        self.outfd = outfd
        # all done
        return

    def __str__(self):
        # build a human readable representation
        return f"pipe in={self.infd}, out={self.outfd}"


# end of file
