# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Constraint import Constraint


class Not(Constraint):
    """
    Given a constraint, a candidate satisfies this if it fails the constraint
    """


    def validate(self, candidate):
        try:
            self.constraint.validate(candidate)
        except self.constraint.ConstraintViolationError:
            return candidate

        raise self.ConstraintViolationError(self, candidate)


    def __init__(self, constraint, **kwds):
        super().__init__(**kwds)
        self.constraint = constraint
        return


    def __str__(self):
        return "not {0.constraint}".format(self)


# end of file 
