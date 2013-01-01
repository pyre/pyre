# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


from .Constraint import Constraint


class Subset(Constraint):
    """
    Given a set S, a candidate set satisfies this constraint iff it is a subset of S
    """


    def validate(self, candidate):
        if self.choices.issuperset(candidate):
            return candidate

        raise self.ConstraintViolationError(self, candidate)


    def __init__(self, choices, **kwds):
        super().__init__(**kwds)
        self.choices = set(choices)
        return


    def __str__(self):
        return "a subset of {0!r}".format(self.choices)


# end of file 
