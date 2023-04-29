# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


"""
Definitions for all the exceptions raised by this package
"""


# superclass
from ..framework.exceptions import FrameworkError


# the local base
class H5Error(FrameworkError):
    """
    The base class of all exceptions raised by the h5 package
    """


# end of file
