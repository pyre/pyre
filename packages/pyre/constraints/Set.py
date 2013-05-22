# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# superclass
from .Constraint import Constraint


# declaration
class Set(Constraint):
    """
    Check whether the candidate is a member of a given set
    """


    # interface
    def validate(self, candidate):
        """
        Check whether {candidate} satisfies this constraint
        """
        # if {candidate} is one of my values
        if candidate in self.choices:
            # indicate success
            return candidate
        # otherwise, fail
        raise self.ConstraintViolationError(self, candidate)


    # meta-methods
    def __init__(self, *choices, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my choices
        self.choices = set(choices)
        # all done
        return


    def __str__(self):
        return "a member of {!r}".format(self.choices)


# end of file 
