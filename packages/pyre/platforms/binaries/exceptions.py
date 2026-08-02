# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Definitions for all the exceptions raised by this package
"""

# the framework wide base error
from ...framework.exceptions import FrameworkError


# the local base
class BinaryError(FrameworkError):
    """
    Base class for all errors raised while reading binary images
    """


# unreadable images
class FormatError(BinaryError):
    """
    Exception raised when a file is not an image in a format this package understands
    """

    # the error message template
    description = "'{0.path}': {0.problem}"

    # meta-methods
    def __init__(self, path, problem, **kwds):
        # chain up
        super().__init__(**kwds)
        # record the offending file
        self.path = path
        # and what is wrong with it
        self.problem = problem
        # all done
        return


# end of file
