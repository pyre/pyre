# -*- coding: utf-8 -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             michael a.g. aïvázis
#                                  orthologue
#                      (c) 1998-2009  all rights reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from .Constraint import Constraint


class GreaterEqual(Constraint):


    def validate(self, candidate):
        if candidate >= self.value:
            return candidate

        raise self.ConstraintViolationError(self, candidate)


    def __init__(self, value, **kwds):
        super().__init__(**kwds)
        self.value = value
        return


    def __str__(self):
        return "greater than or equal to {0!r}".format(self.value)


# end of file 
