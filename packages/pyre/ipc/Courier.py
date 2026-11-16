# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# externals
import os

# support
import journal


# declaration
class Courier(journal.courier):
    """
    The journal device that ships entries down a channel

    The journal's courier writes to a descriptor, and closes it when it is done; this one gives
    it a copy of the writable end of a channel, so that the channel and the courier each close
    their own, and neither depends on the other staying alive
    """

    # metamethods
    def __init__(self, channel, **kwds):
        # chain up, with a copy of the writable end of the {channel}
        super().__init__(descriptor=os.dup(channel.outbound), **kwds)
        # all done
        return


# end of file
