# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Constraint import Constraint


# declaration
class NonEmpty(Constraint):
    """
    Constraint that is satisfied when the candidate container has at least one element
    """

    # interface
    def validate(self, value, **kwds):
        """
        Check whether {value} satisfies this constraint
        """
        # if {value} has at least one element
        if len(value) > 0:
            # indicate success
            return value
        # otherwise, chain up
        return super().validate(value=value, **kwds)

    # meta-methods
    def __str__(self):
        return "a non-empty container"


# end of file
