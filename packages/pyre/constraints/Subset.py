# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# superclass
from .Constraint import Constraint


# declaration
class Subset(Constraint):
    """
    Constraint that is satisfied when the candidate is a subset of a given set
    """


    # interface
    def validate(self, candidate):
        """
        Check whether {candidate} satisfies this constraint
        """
        # if my set is a superset of {candidate}
        if self.choices.issuperset(candidate):
            # indicate success
            return candidate
        # otherwise, fail
        raise self.ConstraintViolationError(self, candidate)


    # meta-methods
    def __init__(self, choices, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my choices
        self.choices = set(choices)
        # all done
        return


    def __str__(self):
        return "a subset of {!r}".format(self.choices)


# end of file 
