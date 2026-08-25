# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import socket

# my base class
from .Socket import Socket


# declaration
class SocketPair(Socket):
    """
    A channel implemented over one end of a connected pair of unix domain sockets

    Socket pairs are anonymous: they are born connected, so there is nothing to name, bind to,
    or accept. They deliver everything {Pipe} does over a single descriptor per side, and add
    the one trick unique to unix domain sockets: open file descriptors can travel across, so
    one process can grant another access to a file or socket it has opened
    """

    # constants
    family = socket.AF_UNIX
    type = socket.SOCK_STREAM

    # factories
    @classmethod
    def open(cls, **kwds):
        """
        Build a pair of connected channels suitable for bidirectional communication between
        two processes on the same host
        """
        # ask the kernel for a connected pair of unix domain stream sockets
        one, two = socket.socketpair(cls.family, cls.type)
        # rewrap each raw socket as a channel by stealing its descriptor
        parent = cls(cls.family, cls.type, 0, fileno=one.detach())
        child = cls(cls.family, cls.type, 0, fileno=two.detach())
        # mirror the {Pipe} contract: the parent side does not survive the {exec} family of
        # spawners, while the child side is inheritable so it can be handed to a new process
        parent.set_inheritable(False)
        child.set_inheritable(True)
        # hand off the pair
        return parent, child

    # interface
    def sendDescriptors(self, descriptors, payload=b"\x00"):
        """
        Ship copies of the open file {descriptors} to my peer, along with a small {payload}

        The {payload} must be at least one byte long: ancillary data cannot ride on an empty
        message. The peer receives duplicates, so both processes hold the descriptors open
        until each closes its own copy
        """
        # delegate to the wrapper in the standard library, which speaks {SCM_RIGHTS}
        return socket.send_fds(self, [payload], descriptors)

    def recvDescriptors(self, limit, maxlen=1):
        """
        Receive up to {limit} open file descriptors from my peer, along with up to {maxlen}
        bytes of the payload of the message that carried them
        """
        # delegate to the wrapper in the standard library
        payload, descriptors, _, _ = socket.recv_fds(self, maxlen, limit)
        # hand off the payload and the descriptors
        return payload, list(descriptors)

    # meta-methods
    def __str__(self):
        """build a human readable representation"""
        return f"socket pair endpoint at fd {self.fileno()}"

    # implementation details
    __slots__ = ()  # socket has it, so why not...


# end of file
