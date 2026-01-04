# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Channel import Channel


# the manager of a debug channel
class Warning(Channel, family="pyre.journal.warning"):
    """
    The manager of a warning channel
    """

    # constants
    severity = "warning"


# end of file
