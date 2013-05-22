# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# superclass
from .Constraint import Constraint


# declaration
class Comparison(Constraint):
    """
    Base class for constraints that compare candidates against values
    """

    # my comparison operator and its textual representation
    tag = None
    compare = None


    # interface
    def validate(self, candidate):
        """
        Check whether {candidate} satisfies this constraint
        """
        # if {candidate} compares correctly with my value
        if self.compare(candidate, self.value):
            # indicate success
            return candidate
        # otherwise, fail
        raise self.ConstraintViolationError(self, candidate)


    # meta-methods
    def __init__(self, value, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my reference value
        self.value = value
        # all done
        return


    def __str__(self):
        return "{0.tag} {0.value!r}".format(self)


# end of file 
