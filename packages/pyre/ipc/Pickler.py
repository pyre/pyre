# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis, leif strand
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# externals
import pyre
import pickle
import struct

from .Marshaller import Marshaller


class Pickler(pyre.component, family="pyre.ipc.marshallers.pickler", implements=Marshaller):
    """
    A marshaller that uses the native python services in {pickle} to serialize python objects
    for transmission to other processes.

    The {send} protocol pickles an object into the payload byte stream, and builds a header
    with the length of the payload. Similarly, {read} first extracts the length of the byte
    string and uses that information to pull the object representation from the input
    channel. This is necessary because pickle reads aggressively from input streams and
    discards any unused information, leading to stream corruption.
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
        # if i got nothing, bail out
        if not header: return None
        # unpack it
        length, = struct.unpack(self.packing, header)
        # get the body
        body = channel.read(length)
        # in as many attempts as it takes
        while len(body) < length:
            # keep accumulating
            body += self.read(length - len(body))
        # extract the object and return it
        return pickle.loads(body) 
                             

# end of file 
