# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import pyre
import pickle
import struct

# my protocol
from . import marshaler

# the marker for conversations cut short
from .exceptions import EndOfStream


# class declaration
class Pickler(pyre.component, family="pyre.ipc.marshalers.pickler", implements=marshaler):
    """
    A marshaler that uses the native python services in {pickle} to serialize python objects
    for transmission to other processes.

    The {send} protocol pickles an object into the payload byte stream, and builds a header
    with the length of the payload. Similarly, {recv} first extracts the length of the byte
    string and uses that information to pull the object representation from the input
    channel. This is necessary to simplify interacting with streams that may make only portions
    of their contents available at a time.
    """

    # public data
    packing = "<L"  # the struct format for encoding the payload length
    headerSize = struct.calcsize(packing)

    # interface
    @pyre.export
    def send(self, item, channel):
        """
        Pack and ship {item} over {channel}
        """
        # pickle the item
        body = pickle.dumps(item)
        # build its header
        header = struct.pack(self.packing, len(body))
        # put it together
        message = header + body
        # send it off
        return channel.write(bytes=message)

    @pyre.export
    def recv(self, channel):
        """
        Extract and return a single item from {channel}

        Raises {EndOfStream} when the channel closes before a complete message arrives,
        whether cleanly between messages or mid-transmission
        """
        # get the length; insist on a complete header, since it may arrive in pieces even
        # from a healthy peer, and read exactly the header, since overreading would swallow
        # the beginning of whatever follows in the stream
        header = channel.read(minlen=self.headerSize, maxlen=self.headerSize)
        # if the channel ran dry before the header completed
        if len(header) < self.headerSize:
            # the conversation is over
            raise EndOfStream(channel=channel, received=len(header), expected=self.headerSize)
        # unpack it
        (length,) = struct.unpack(self.packing, header)
        # get the body, again reading exactly what the header promised
        body = channel.read(minlen=length, maxlen=length)
        # if the channel ran dry mid-message
        if len(body) < length:
            # the peer died while transmitting
            raise EndOfStream(channel=channel, received=len(body), expected=length)
        # extract the object and return it
        return pickle.loads(body)


# end of file
