# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis, leif strand
# orthologue
# (c) 1998-2013 all rights reserved
#


# externals
import pyre
import pickle
import struct

from .protocols import marshaller


class Pickler(pyre.component, family="pyre.ipc.marshallers.pickler", implements=marshaller):
    """
    A marshaller that uses the native python services in {pickle} to serialize python objects
    for transmission to other processes.

    The {send} protocol pickles an object into the payload byte stream, and builds a header
    with the length of the payload. Similarly, {read} first extracts the length of the byte
    string and uses that information to pull the object representation from the input
    channel. This is necessary to simplify interacting with buffered streams.
    """ 


    # public data
    packing = "<L" # the struct format for encoding the payload length


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
        return channel.write(bstr=message)


    @pyre.export
    def recv(self, channel):
        """
        Extract and return a single item from {channel}
        """
        # get the length
        header = channel.read(struct.calcsize(self.packing))
        # unpack it
        length, = struct.unpack(self.packing, header)
        # get the body
        body = channel.read(length)
        # extract the object and return it
        return pickle.loads(body) 
                             

# end of file 
