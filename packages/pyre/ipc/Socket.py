# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import socket

# my interface
from .Channel import Channel


# declaration
class Socket(socket.socket, Channel):
    """
    A channel that uses sockets as the communication mechanism

    This class captures the part of the {socket} interface that is independent of the type of
    socket. The implementation of the remainder of the {Channel} interface is provided by
    subclasses.
    """

    # types
    from ..schemata import inet

    # access to the individual channel end points
    @property
    def inbound(self):
        """
        Retrieve the channel end point that can be read
        """
        # easy enough
        return self

    @property
    def outbound(self):
        """
        Retrieve the channel end point that can be written
        """
        # easy enough
        return self

    # access to the socket properties
    @property
    def peer(self):
        """
        Return the address of my peer, i.e. the remote endpoint of the socket
        """
        # attempt to
        try:
            # get the raw address
            address = self.getpeername()
        # if something goes wrong
        except OSError:
            # make an empty address and send it off
            return self.inet()

        # otherwise, parse the address, decorate it and return it
        return self.inet().recognize(family=self.family, address=address)

    # input/output
    # these implementations assume stream semantics; datagram flavors must override
    def read(self, minlen=0, maxlen=4 * 1024):
        """
        Read {count} bytes from my input channel
        """
        # make sure
        if maxlen < minlen:
            # that the input parameters are sane
            maxlen = minlen
        # reset the byte count
        total = 0
        # initialize the packet pile
        packets = []
        # for as long as it takes
        while True:
            # carefully
            try:
                # pull something from the channel
                packet = self.recv(maxlen - total)
            # if the peer closed the connection
            except ConnectionResetError:
                # bail
                break

            # otherwise, get the packet length
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

    def write(self, bytes):
        """
        Write the {bytes} to my output channel
        """
        # make sure the entire byte string is delivered
        self.sendall(bytes)
        # and return the number of bytes sent
        return len(bytes)

    # interface
    def accept(self):
        """
        Wait for a connection attempt, build a channel around the socket to the peer, and
        return it along with the address of the remote process
        """
        # bypass the socket interface because it calls the wrong constructor explicitly
        fd, address = self._accept()
        # build the channel
        channel = type(self)(self.family, self.type, self.proto, fileno=fd)
        # build the address
        address = self.inet().recognize(family=self.family, address=address)
        # adjust the socket flags; see {socket.py} in the standard library for more details
        if socket.getdefaulttimeout() is None and self.gettimeout():
            channel.setblocking(True)
        # return the channel to and the address of the peer process
        return channel, address

    # meta-methods
    def __str__(self):
        return f"socket to {self.peer}"

    # implementation details
    __slots__ = ()  # socket has it, so why not...


# end of file
