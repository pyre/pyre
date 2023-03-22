# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import pyre

# my protocol
from .Tools import Tools


# declaration
class POSIXTools(pyre.component, family="pyre.platforms.tools.posix", implements=Tools):
    """
    Commonly used POSIX tools and their options
    """


# end of file
