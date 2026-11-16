# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# declaration
class Message:
    """
    The base class of what the staffing agency and its liaison say to each other

    A message travels over the control channel as one marshaled object; the channels it holds,
    if any, travel inside it
    """

    # interface
    def send(self, channel, marshaler) -> "Message":
        """
        Ship me over {channel}, with {marshaler}
        """
        # easy enough
        marshaler.send(item=self, channel=channel)
        # all done
        return self

    @classmethod
    def receive(cls, channel, marshaler) -> "Message":
        """
        Take delivery of the next message on {channel}, read with {marshaler}
        """
        # easy enough
        return marshaler.recv(channel=channel)

    def deliver(self, recipient):
        """
        Hand me to the method of {recipient} that handles messages of my kind
        """
        # every kind of message knows its handler
        raise NotImplementedError(f"class '{type(self).__name__}' must implement 'deliver'")


# end of file
