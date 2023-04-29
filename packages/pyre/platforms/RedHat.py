# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from .Linux import Linux


# declaration
class RedHat(Linux, family="pyre.platforms.redhat"):
    """
    Encapsulation of a host running linux on the ubuntu distribution
    """

    # public data
    distribution = "redhat"


# end of file
