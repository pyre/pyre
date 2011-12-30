# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


from .Constraint import Constraint


class Between(Constraint):
    """
    Given a and b from a set with an ordering principle, this constraint is satisfied if x is
    in (a,b)
    """


    def validate(self, candidate):
        if candidate > self.low and candidate < self.high:
            return candidate

        raise self.ConstraintViolationError(self, candidate)


    def __init__(self, low, high, **kwds):
        super().__init__(**kwds)
        self.low = low
        self.high = high
        return


    def __str__(self):
        return "between {0.low} and {0.high}".format(self)


# end of file 
