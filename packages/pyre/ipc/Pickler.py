# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import io
import pickle
import struct

# support
import pyre

# my protocol
from . import marshaler

# the record of the channels that travel in a message
from .Manifest import Manifest

# the marker for conversations cut short
from .exceptions import EndOfStream


# class declaration
class Pickler(pyre.component, family="pyre.ipc.marshalers.pickler", implements=marshaler):
    """
    A marshaler that uses the native python services in {pickle} to serialize python objects
    for transmission to other processes.

    The {send} protocol pickles an object into the payload byte stream, and builds a header
    with the length of the payload and the number of open descriptors that travel with it.
    Similarly, {recv} first extracts the header and uses it to pull the object representation
    from the input channel, along with its descriptors. This is necessary to simplify
    interacting with streams that may make only portions of their contents available at a
    time.

    Channels inside the object travel whole: pickle hands them to the manifest of the message,
    which encodes each one as a token, and the channel the message goes over carries their
    descriptors
    """

    # public data
    # the struct format for encoding the payload length and the descriptor count
    packing = "<LL"
    # and the size of the header it makes
    headerSize = struct.calcsize(packing)

    # interface
    @pyre.export
    def send(self, item, channel):
        """
        Pack and ship {item} over {channel}, and hand back the manifest of the message, which
        names the channels that travelled inside it
        """
        # the record of the channels in the item
        manifest = Manifest()
        # make room for the pickle
        stream = io.BytesIO()
        # make a pickler
        pickler = pickle.Pickler(stream)
        # that hands every channel it meets to the manifest
        pickler.persistent_id = manifest.declare
        # pickle the item
        pickler.dump(item)
        # get the payload
        body = stream.getvalue()
        # build its header
        header = struct.pack(self.packing, len(body), len(manifest.descriptors))
        # send it off, along with the descriptors of the channels in the item
        channel.write(bytes=header + body, descriptors=manifest.descriptors)
        # and hand back the record of the channels that travelled
        return manifest

    @pyre.export
    def recv(self, channel):
        """
        Extract and return a single item from {channel}

        Raises {EndOfStream} when the channel closes before a complete message arrives,
        whether cleanly between messages or mid-transmission
        """
        # get the header; insist on a complete one, since it may arrive in pieces even from a
        # healthy peer, and read exactly the header, since overreading would swallow the
        # beginning of whatever follows in the stream
        header = channel.read(minlen=self.headerSize, maxlen=self.headerSize)
        # if the channel ran dry before the header completed
        if len(header) < self.headerSize:
            # the conversation is over
            raise EndOfStream(channel=channel, received=len(header), expected=self.headerSize)
        # unpack it
        length, count = struct.unpack(self.packing, header)
        # get the body, again reading exactly what the header promised
        body = channel.read(minlen=length, maxlen=length)
        # if the channel ran dry mid-message
        if len(body) < length:
            # the peer died while transmitting
            raise EndOfStream(channel=channel, received=len(body), expected=length)
        # collect the descriptors that came with the message
        manifest = Manifest(descriptors=channel.claim(count=count))
        # make an unpickler
        unpickler = pickle.Unpickler(io.BytesIO(body))
        # that asks the manifest to rebuild every channel in the item
        unpickler.persistent_load = manifest.claim
        # extract the object and return it
        return unpickler.load()


# end of file
