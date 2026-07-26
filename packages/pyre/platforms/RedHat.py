# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# framework
import pyre

# superclass
from .Linux import Linux


# declaration
class RedHat(Linux, family="pyre.platforms.redhat"):
    """
    Encapsulation of a host running linux on the ubuntu distribution
    """

    # public data
    distribution = "redhat"

    # user configurable state
    packagers = pyre.properties.strings()
    packagers.default = ["conda", "rpm", "bare"]
    packagers.doc = "the ordered stack of package databases to interrogate, most specific first"


# end of file
