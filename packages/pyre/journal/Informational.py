# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# superclass
from .Channel import Channel


# the manager of a debug channel
class Informational(Channel, family="pyre.journal.info"):
    """
    The manager of an info channel
    """

    # constants
    severity = "info"


# end of file
