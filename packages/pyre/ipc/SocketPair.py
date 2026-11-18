# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import errno
import os
import resource
import socket

# my base class
from .Socket import Socket

# the exceptions raised when descriptors cannot be carried, or did not arrive
from .exceptions import ArrivalError, CarriageError


# declaration
class SocketPair(Socket):
    """
    A channel implemented over one end of a connected pair of unix domain sockets

    Socket pairs are anonymous: they are born connected, so there is nothing to name, bind to,
    or accept. They deliver everything {Pipe} does over a single descriptor per side, and add
    the one trick unique to unix domain sockets: open file descriptors can travel across, so
    one process can grant another access to a file or socket it has opened

    Descriptors travel with the bytes they are written with, and arrive with the first of
    them; every read collects whatever arrives, and keeps it until it is claimed. A process
    whose descriptor table is full receives the bytes without their descriptors, and the claim
    that finds them missing says so
    """

    # constants
    # my address family
    family = socket.AF_UNIX
    # and my type
    type = socket.SOCK_STREAM
    # the most descriptors that may travel with one write
    capacity = 64

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
        # on both sides
        child = cls(cls.family, cls.type, 0, fileno=two.detach())
        # mirror the {Pipe} contract: the parent side does not survive the {exec} family of
        # spawners, while the child side is inheritable so it can be handed to a new process
        parent.set_inheritable(False)
        # and the child side is
        child.set_inheritable(True)
        # hand off the pair as labeled endpoints, so the order is part of the contract
        return cls.ends(parent=parent, child=child)

    # input/output
    def receive(self, count):
        """
        Pull up to {count} bytes from the socket, and keep the descriptors that arrive with them

        When my descriptor table is full, the bytes arrive without their descriptors, and
        nothing is recorded about the loss; the claim that finds them missing reports it
        """
        # until the bytes come through
        while True:
            # carefully
            try:
                # read, making room for as many descriptors as a write may carry
                data, descriptors, _, _ = socket.recv_fds(self, count, self.capacity)
            # if the read was refused
            except OSError as error:
                # because the descriptors that came with the bytes had no room, which is how
                # some kernels report a full descriptor table after dropping the descriptors
                if error.errno == errno.EMSGSIZE:
                    # the bytes are still there, so read again
                    continue
                # anything else is not mine to handle
                raise
            # got the bytes
            break
        # keep the descriptors until they are claimed
        self.arrivals.extend(descriptors)
        # and hand off the bytes
        return data

    def write(self, bytes, descriptors=()):
        """
        Write the {bytes} to my peer, along with the open file {descriptors}, if any
        """
        # without descriptors
        if not descriptors:
            # this is an ordinary write
            return super().write(bytes=bytes)
        # if there are more than my peer has room for
        if len(descriptors) > self.capacity:
            # refuse
            raise CarriageError(
                channel=self, reason=f"{len(descriptors)} is more than {self.capacity} at once"
            )
        # send the descriptors, along with as many of the bytes as the socket takes at once
        sent = socket.send_fds(self, [bytes], list(descriptors))
        # if the socket did not take them all
        if sent < len(bytes):
            # make sure the rest follow
            self.sendall(bytes[sent:])
        # report the number of bytes sent
        return len(bytes)

    def claim(self, count):
        """
        Take the {count} descriptors that arrived with the bytes just read

        When fewer arrived, which happens when my descriptor table was full, the ones that did
        are closed, and {ArrivalError} is raised
        """
        # if fewer arrived than were sent
        if len(self.arrivals) < count:
            # get the ones that did
            arrived = self.arrivals[:]
            # forget them
            self.arrivals.clear()
            # go through them
            for descriptor in arrived:
                # and close each one, since a message without all of its channels is lost
                os.close(descriptor)
            # look up the most files this process may hold open
            limit, _ = resource.getrlimit(resource.RLIMIT_NOFILE)
            # and complain
            raise ArrivalError(channel=self, expected=count, received=len(arrived), limit=limit)
        # otherwise, take the ones asked for
        claimed = self.arrivals[:count]
        # and keep the rest
        del self.arrivals[:count]
        # hand them off
        return claimed

    # descriptor delegation
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
    def __init__(self, family=-1, type=-1, proto=-1, fileno=None, **kwds):
        # chain up
        super().__init__(family=family, type=type, proto=proto, fileno=fileno, **kwds)
        # the descriptors that arrived and are not yet claimed
        self.arrivals = []
        # all done
        return

    def __str__(self):
        """
        Build a human readable representation
        """
        # easy enough
        return f"socket pair endpoint at fd {self.fileno()}"

    # implementation details
    __slots__ = ("arrivals",)


# end of file
