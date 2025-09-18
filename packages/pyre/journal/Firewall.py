# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# support
import pyre

# superclass
from .Channel import Channel


# the manager of a debug channel
class Firewall(Channel, family="pyre.journal.firewall"):
    """
    The manager of a firewall
    """

    # constants
    severity = "firewall"

    # user configurable state
    fatal = pyre.properties.bool()
    fatal.default = True
    fatal.doc = "control whether hitting the firewall terminates the app"


# end of file
