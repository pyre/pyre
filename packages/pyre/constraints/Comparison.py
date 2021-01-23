# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# superclass
from .Constraint import Constraint


# base class for all comparison constraints
class Comparison(Constraint):
    """
    Base class for constraints that compare candidates against values
    """

    # my comparison operator
    compare = None
    # and its textual representation
    tag = None


    # interface
    def validate(self, value, **kwds):
        """
        Check whether {value} satisfies this constraint
        """
        # if {value} compares correctly with my value
        if self.compare(value, self.value):
            # indicate success
            return value
        # otherwise, chain up
        return super().validate(value=value, **kwds)


    # metamethods
    def __init__(self, value, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my reference value
        self.value = value
        # all done
        return


    def __str__(self):
        # build the representation
        return f"{self.tag} '{self.value}'"


# end of file
