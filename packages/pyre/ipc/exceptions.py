# -*- python -*-
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


# signals cannot reach the event loop
class SignalRelayError(IPCError):
    """
    The relay that delivers signals to event loops could not take charge of a signal

    The interpreter lets only its main thread install signal handlers and the descriptor it
    writes to when a signal arrives, and it keeps a single such descriptor per process, so the
    relay refuses when asked from another thread, or when somebody else, e.g. an {asyncio}
    event loop, already owns the descriptor
    """

    # the message template
    description = "cannot relay signal {0.signal} to the event loop: {0.reason}"

    # metamethods
    def __init__(self, signal, reason, **kwds):
        # chain up
        super().__init__(**kwds)
        # the signal that was asked for
        self.signal = signal
        # and why it cannot be relayed
        self.reason = reason
        # all done
        return


# end of file
