# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Constraint import Constraint


class And(Constraint):
    """
    Given a set of contraints, $x$ satisfies this iff it satisfies all the constraints in the set
    """


    def validate(self, candidate):
        for constraint in self.constraints:
            constraint.validate(candidate)

        return candidate


    def __init__(self, *constraints, **kwds):
        super().__init__(**kwds)
        self.constraints = constraints
        return


    def __str__(self):
        return " and ".join("({0})".format(constraint) for constraint in self.constraints)


# end of file 
