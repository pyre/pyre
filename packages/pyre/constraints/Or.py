# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


from .Constraint import Constraint


class Or(Constraint):
    """
    Given a set of constraints, a candidate satisfies this iff it satisfies any of the constraints
    """


    def validate(self, candidate):
        for constraint in self.constraints:
            try:
                return constraint.validate(candidate)
            except constraint.ConstraintViolationError:
                continue

        raise self.ConstraintViolationError(self, candidate)


    def __init__(self, *constraints, **kwds):
        super().__init__(**kwds)
        self.constraints = constraints
        return


    def __str__(self):
        return " or ".join("({0})".format(constraint) for constraint in self.constraints)


# end of file 
