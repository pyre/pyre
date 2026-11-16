# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the travelers
from .Channel import Channel


# declaration
class Manifest:
    """
    The record of the channels that travel inside one message

    A marshaler that meets a channel while encoding a message declares it here, and encodes the
    token it gets back in the channel's place; the descriptors of every channel declared travel
    with the message. On arrival, the marshaler gives each token back, and the channel is
    rebuilt from the descriptors that came with the message. Marshalers connect a manifest to
    whatever hook their serializer offers for objects that are not encoded by value, so channels
    know nothing about marshalers, and marshalers nothing about each other
    """

    # interface
    def declare(self, item) -> dict | None:
        """
        If {item} is a channel, record it, and hand back the token to encode in its place;
        anything else is encoded by value
        """
        # only channels travel this way
        if not isinstance(item, Channel):
            # everything else is left to the marshaler
            return None
        # ask the channel how it leaves
        hints, descriptors = item.depart()
        # its descriptors go after the ones already declared
        first = len(self.descriptors)
        # add them to the pile
        self.descriptors.extend(descriptors)
        # and hand back what the far side needs to find them
        return {"hints": hints, "first": first, "count": len(descriptors)}

    def claim(self, token: dict) -> Channel:
        """
        Rebuild the channel described by {token} from the descriptors that arrived
        """
        # get the position of its descriptors
        first = token["first"]
        # pick them out
        descriptors = self.descriptors[first : first + token["count"]]
        # and rebuild the channel
        return Channel.arrive(hints=token["hints"], descriptors=descriptors)

    # metamethods
    def __init__(self, descriptors=(), **kwds):
        # chain up
        super().__init__(**kwds)
        # the descriptors of the channels in the message, in the order they were declared
        self.descriptors = list(descriptors)
        # all done
        return


# end of file
