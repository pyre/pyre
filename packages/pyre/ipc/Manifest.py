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
    rebuilt from the descriptors that came with the message. The sender's own channels are
    still open after the message leaves, and the manifest of the message names them, so the
    sender can release the ones it no longer needs. A channel that appears more than once in a
    message travels once, and arrives as a single channel, the way any object shared within a
    message does. Marshalers connect a manifest to whatever hook their serializer offers for
    objects that are not encoded by value, so channels know nothing about marshalers, and
    marshalers nothing about each other
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
        # look for the token of a channel declared already
        token = self.tokens.get(id(item))
        # if there is one
        if token is not None:
            # the channel travels once, so encode the same token again
            return token
        # otherwise, ask the channel how it leaves
        hints, descriptors = item.depart()
        # its descriptors go after the ones already declared
        first = len(self.descriptors)
        # add them to the pile
        self.descriptors.extend(descriptors)
        # build what the far side needs to find them, and to recognize the channel when it
        # meets it again
        token = {
            "hints": hints,
            "index": len(self.channels),
            "first": first,
            "count": len(descriptors),
        }
        # record the channel, which also keeps it alive while its identity is in use
        self.channels.append(item)
        # and its token
        self.tokens[id(item)] = token
        # hand off the token
        return token

    def claim(self, token: dict) -> Channel:
        """
        Rebuild the channel described by {token} from the descriptors that arrived, once, and
        hand back the same channel every time the message names it
        """
        # get the channel's place in the message
        index = token["index"]
        # look for it among the ones rebuilt already
        channel = self.arrivals.get(index)
        # if it's there
        if channel is not None:
            # hand it back
            return channel
        # otherwise, get the position of its descriptors
        first = token["first"]
        # pick them out
        descriptors = self.descriptors[first : first + token["count"]]
        # rebuild the channel
        channel = Channel.arrive(hints=token["hints"], descriptors=descriptors)
        # remember it
        self.arrivals[index] = channel
        # and hand it off
        return channel

    # metamethods
    def __init__(self, descriptors=(), **kwds):
        # chain up
        super().__init__(**kwds)
        # the channels declared in a message on its way out, in the order they were declared
        self.channels = []
        # their tokens, by the identity of each channel
        self.tokens = {}
        # the descriptors of the channels in the message, in the same order
        self.descriptors = list(descriptors)
        # and the channels rebuilt from them on arrival, by their place in the message
        self.arrivals = {}
        # all done
        return


# end of file
