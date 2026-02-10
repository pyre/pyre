# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Linux import Linux


# declaration
class Fedora(Linux, family="pyre.platforms.fedora"):
    """
    Encapsulation of a host running linux on the fedora distribution
    """

    # public data
    distribution = "fedora"


# end of file
