# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# declaration
class Message:
    """
    The base class of what the staffing agency and its liaison say to each other

    A message travels over the control channel as one marshaled object; the open descriptors it
    carries, if any, ride right after it, as ancillary data on a byte of their own, since a
    marshaled stream has no room for them
    """

    # interface
    def send(self, channel, marshaler) -> "Message":
        """
        Ship me over {channel}, with {marshaler}, followed by my descriptors
        """
        # the message itself
        marshaler.send(item=self, channel=channel)
        # if it carries descriptors
        if self.descriptors:
            # they follow it
            channel.sendDescriptors(descriptors=self.descriptors)
        # all done
        return self

    @classmethod
    def receive(cls, channel, marshaler) -> "Message":
        """
        Take delivery of the next message on {channel}, read with {marshaler}, along with the
        descriptors it carries
        """
        # get the message
        message = marshaler.recv(channel=channel)
        # if it announces descriptors
        if message.descriptors:
            # collect them; the ones that travelled with the message are the sender's numbers,
            # and mean nothing here
            _, message.descriptors = channel.recvDescriptors(limit=len(message.descriptors))
        # hand it off
        return message

    def deliver(self, recipient):
        """
        Hand me to the method of {recipient} that handles messages of my kind
        """
        # every kind of message knows its handler
        raise NotImplementedError(f"class '{type(self).__name__}' must implement 'deliver'")

    # metamethods
    def __init__(self, descriptors=(), **kwds):
        # chain up
        super().__init__(**kwds)
        # the open descriptors that travel with me
        self.descriptors = list(descriptors)
        # all done
        return


# end of file
