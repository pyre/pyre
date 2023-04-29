# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from .Linux import Linux


# declaration
class CentOS(Linux, family="pyre.platforms.centos"):
    """
    Encapsulation of a host running linux on the centos distribution
    """

    # public data
    distribution = "centos"


# end of file
