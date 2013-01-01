# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


from .Constraint import Constraint


class LessEqual(Constraint):
    """
    Given $a$, candidate $x$ satisfies this constraint if $x <= a$
    """


    def validate(self, candidate):
        if candidate <= self.value:
            return candidate

        raise self.ConstraintViolationError(self, candidate)


    def __init__(self, value, **kwds):
        super().__init__(**kwds)
        self.value = value
        return


    def __str__(self):
        return "less than or equal to {0!r}".format(self.value)


# end of file 
