# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# support
import pyre

# superclass
from .Channel import Channel


# the manager of a debug channel
class Debug(Channel, family="pyre.journal.debug"):
    """
    The manager of a debug channel
    """

    # constants
    severity = "debug"

    # user configurable state
    active = pyre.properties.bool()
    active.default = False
    active.doc = "control whether the channel produces output"


# end of file
