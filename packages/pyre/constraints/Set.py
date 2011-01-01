# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Constraint import Constraint


class Set(Constraint):
    """
    Given a set, a candidate satisfies this constraint if it is a member of the set
    """


    def validate(self, candidate):
        if candidate in self.choices:
            return candidate

        raise self.ConstraintViolationError(self, candidate)


    def __init__(self, *choices, **kwds):
        super().__init__(**kwds)
        self.choices = set(choices)
        return


    def __str__(self):
        return "a member of {0!r}".format(self.choices)


# end of file 
