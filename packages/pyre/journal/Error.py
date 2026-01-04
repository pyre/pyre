# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# superclass
from .Channel import Channel


# the manager of a debug channel
class Error(Channel, family="pyre.journal.error"):
    """
    The manager of an error channel
    """

    # constants
    severity = "error"

    # user configurable state
    fatal = pyre.properties.bool()
    fatal.default = True
    fatal.doc = "control whether writing to the channel terminates the app"


# end of file
