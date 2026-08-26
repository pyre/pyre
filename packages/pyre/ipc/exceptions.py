# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# exceptions
from ..framework.exceptions import FrameworkError


# local anchor
class IPCError(FrameworkError):
    """
    Base exception for all error conditions detected by ipc components
    """


# the channel closed mid-conversation
class EndOfStream(IPCError):
    """
    The channel was closed by its peer before a complete message arrived

    Marshalers raise this when a read comes up short: either the channel closed cleanly
    between messages, or the peer died mid-transmission. Either way, no further messages are
    coming, and the caller should treat the conversation as over
    """

    # the message template
    description = "end of stream: received {0.received} of {0.expected} bytes"

    # metamethods
    def __init__(self, channel=None, received=0, expected=0, **kwds):
        # chain up
        super().__init__(**kwds)
        # the channel that ran dry
        self.channel = channel
        # how much of the message made it
        self.received = received
        # and how much was promised
        self.expected = expected
        # all done
        return


# end of file
