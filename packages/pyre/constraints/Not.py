# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# superclass
from .Constraint import Constraint


# op!
class Not(Constraint):
    """
    Constraint that is satisfied when the candidate fails to satisfy a given constraint
    """


    # interface
    def validate(self, value, **kwds):
        """
        Check whether {value} satisfies this constraint
        """
        # check
        try:
            # whether my constraint is satisfied
            self.constraint.validate(value=value, **kwds)
        # and if it is not
        except self.constraint.ConstraintViolationError:
            # indicate success
            return value
        # otherwise, chain up
        return super().validate(value=value, **kwds)


    # metamethods
    def __init__(self, constraint, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my constraint
        self.constraint = constraint
        # all done
        return


    def __str__(self):
        # build the representation
        return f"not {self.constraint}"


# end of file
