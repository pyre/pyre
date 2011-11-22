# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis, leif strand
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# externals
import pickle
import struct


class Channel:
    """
    A wrapper around the lower level IPC mechanisms that normalizes the sending and receiving
    of messages. See {Pipe} and {Socket} for concrete examples of encapsulation of the
    operating system services.
    """ 


    # public data
    packing = "<L" # the encoding of the payload length


    # abstract interface
    def read(self, count):
        """
        Read {count} bytes from my input channel
        """
        raise NotImplementedError("class {.__name__!r} must implement 'read'".format(type(self)))


    def write(self, header, body):
        """
        Read {count} bytes from my input channel
        """
        raise NotImplementedError("class {.__name__!r} must implement 'write'".format(type(self)))


    # interface
    def send(self, item):
        """
        Pack and ship {item} over my channel
        """
        # pickle the item
        body = pickle.dumps(item)
        # build its header
        header = struct.pack(self.packing, len(body))
        # send it off
        return self.write(header=header, body=body)


    def recv(self):
        """
        Extract and return a single item from my channel
        """
        # get the length
        header = self.read(struct.calcsize(self.packing))
        # if i got nothing, bail out
        if not header: return None
        # unpack it
        length = struct.unpack(self.packing, header)
        # get the body
        body = self.read(length)
        # in as many attempts as it takes
        while len(body) < length:
            # keep accumulating
            body += self.read(length - len(body))
        # extract the object and return it
        return pickle.loads(body) 
                             

# end of file 
