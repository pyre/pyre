# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# superclass
from .Constraint import Constraint


# set membership
class Set(Constraint):
    """
    Check whether the candidate is a member of a given set
    """


    # interface
    def validate(self, value, **kwds):
        """
        Check whether {value} satisfies this constraint
        """
        # if {value} is one of my values
        if value in self.choices:
            # indicate success
            return value
        # otherwise, chain up
        return super().validate(value=value, **kwds)


    # metamethods
    def __init__(self, *choices, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my choices
        self.choices = set(choices)
        # all done
        return


    def __str__(self):
        # build the representation
        return f"a member of {self.choices}"


# end of file
