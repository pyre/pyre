# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# externals
import re
# superclass
from .Constraint import Constraint


# match against a regex
class Like(Constraint):
    """
    Given a regular expression, a string satisfies this constraint if it matches my regular
    expression
    """


    # interface
    def validate(self, value, **kwds):
        """
        Check whether {value} satisfies this constraint
        """
        # if the value matches my regular expression
        if self.regexp.match(value):
            # indicate success
            return value
        # otherwise, chain up
        return super().validate(value=value, **kwds)


    # metamethods
    def __init__(self, regexp, **kwds):
        # chain up
        super().__init__(**kwds)
        # compile my regular expression
        self.regexp = re.compile(regexp)
        # all done
        return


    def __str__(self):
        # build the representation
        return f"like '{self.regexp.pattern}'"


# end of file
