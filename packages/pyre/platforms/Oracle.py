# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Linux import Linux


# declaration
class Oracle(Linux, family="pyre.platforms.oracle"):
    """
    Encapsulation of a host running Oracle Linux Server
    """

    # public data
    distribution = "oracle"


# end of file
