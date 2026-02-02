# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# leif strand
# (c) 1998-2026 all rights reserved


# declaration
class Channel:
    """
    A wrapper around the lower level IPC mechanisms that normalizes the sending and receiving
    of messages. See {Pipe} and {Socket} for concrete examples of encapsulation of the
    operating system services.
    """

    # interface
    # channel life cycle management
    @classmethod
    def open(cls, **kwds):
        """
        Channel factory
        """
        raise NotImplementedError(f"class '{cls.__name__}' must implement 'open'")

    def close(self):
        """
        Shutdown the channel
        """
        raise NotImplementedError(
            f"class '{type(self).__name__}' must implement 'close'"
        )

    # access to the individual channel end points
    @property
    def inbound(self):
        """
        Retrieve the channel end point that can be read
        """
        raise NotImplementedError(
            f"class '{type(self).__name__}' must implement 'inbound'"
        )

    @property
    def outbound(self):
        """
        Retrieve the channel end point that can be written
        """
        raise NotImplementedError(
            f"class '{type(self).__name__}' must implement 'outbound'"
        )

    # input/output
    def read(self, minlen, maxlen):
        """
        Read up to {maxlen} bytes from my input channel
        """
        raise NotImplementedError(
            f"class '{type(self).__name__}' must implement 'read'"
        )

    def write(self, bytes):
        """
        Write the {bytes} to the output channel
        """
        raise NotImplementedError(
            f"class '{type(self).__name__}' must implement 'write'"
        )


# end of file
