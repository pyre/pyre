# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# superclass
from .Constraint import Constraint


# declaration
class Or(Constraint):
    """
    Given a set of constraints, a candidate satisfies this iff it satisfies any of the constraints
    """


    # interface
    def validate(self, candidate):
        """
        Check whether {candidate} satisfies this constraint
        """
        # go through my constraints
        for constraint in self.constraints:
            # and look for
            try:
                # the first one that is satisfied
                return constraint.validate(candidate)
            # if this one did not
            except constraint.ConstraintViolationError:
                # check the next
                continue
        # if they all failed, fail
        raise self.ConstraintViolationError(self, candidate)


    # meta-methods
    def __init__(self, *constraints, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my constraints
        self.constraints = constraints
        # all done
        return


    def __str__(self):
        return " or ".join("({})".format(constraint) for constraint in self.constraints)


# end of file 
