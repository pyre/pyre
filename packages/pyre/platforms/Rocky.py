# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Linux import Linux


# declaration
class CentOS(Linux, family="pyre.platforms.rocky"):
    """
    Encapsulation of a host running linux on the rocky distribution
    """

    # public data
    distribution = "rocky"


# end of file
