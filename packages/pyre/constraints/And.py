# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# superclass
from .Constraint import Constraint


# logical and
class And(Constraint):
    """
    Meta-constraint that is satisfied when all of its constraints are satisfied
    """


    # interface
    def validate(self, value, **kwds):
        """
        Check whether {value} satisfies this constraint
        """
        # i am happy only if every one of my constraints is happy
        for constraint in self.constraints: constraint.validate(value=value, **kwds)
        # return success
        return value


    # metamethods
    def __init__(self, *constraints, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my list of constraints
        self.constraints = constraints
        # all done
        return


    def __str__(self):
        # build the list of constraint representations
        reps = ( f"({constraint})" for constraint in self.constraints )
        # assemble and return
        return " and ".join(reps)


# end of file
