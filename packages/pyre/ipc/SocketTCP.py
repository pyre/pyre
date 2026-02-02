# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# leif strand
# (c) 1998-2026 all rights reserved


# externals
import socket

# my interface
from .Socket import Socket


# declaration
class SocketTCP(Socket):
    """
    A channel that uses TCP sockets as the communication mechanism
    """

    # constants
    type = socket.SOCK_STREAM

    # input/output
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

    # meta-methods
    def __str__(self):
        """build a human readable representation"""
        return f"tcp socket to {self.peer}"

    # implementation details
    __slots__ = ()  # socket has it, so why not...


# end of file
