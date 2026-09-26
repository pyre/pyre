# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Definitions for all exceptions raised by this package
"""

# framework
import pyre


class Error(pyre.PyreError):
    """
    Exception raised when the cuda support layer detects an error
    """

    # public data
    description = "cuda error"


# end of file
