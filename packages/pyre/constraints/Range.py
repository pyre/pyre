# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Constraint import Constraint


# declaration
class Range(Constraint):
    """
    Given {a} and {b} from a set with an ordering principle, this constraint is satisfied if
    the candidate is in {[a,b)}
    """

    # interface
    def validate(self, value, **kwds):
        """
        Check whether {candidate} satisfies this constraint
        """
        # if {candidate} is between my {low} and my {high}
        if self.low <= value < self.high:
            # indicate success
            return value
        # otherwise, chain up
        return super().validate(value=value, **kwds)

    # metamethods
    def __init__(self, low, high, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my range
        self.low = low
        self.high = high
        # all done
        return

    def __str__(self):
        return f"in [{self.low}, {self.high})"


# end of file
