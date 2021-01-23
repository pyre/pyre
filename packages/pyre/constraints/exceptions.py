# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


"""
Definitions for all the exceptions raised by this package
"""


# the base exception
from ..framework.exceptions import FrameworkError


# base exception
class ConstraintViolationError(FrameworkError):
    """
    Exception used to indicate that a constraint is violated

    Instead of being functions that return booleans, constraints throw exceptions when they are
    violated. This design choice is motivated by the observation that it is not always possible
    to handle a constraint violation locally, since the caller may not have enough information
    to handle the failure.
    """


    # public data
    description  = "{0.value!r} is not {0.constraint}"


    # metamethods
    def __init__(self, constraint, value, **kwds):
        # chain  up
        super().__init__(**kwds)
        # save some context
        self.constraint = constraint
        self.value = value
        # all done
        return


# end of file
