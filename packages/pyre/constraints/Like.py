# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import re
# superclass
from .Constraint import Constraint


# declaration
class Like(Constraint):
    """
    Given a regular expression, a string satisfies this constraint if it matches the regular
    expression
    """


    # interface
    def validate(self, candidate):
        """
        Check whether {candidate} satisfies this constraint
        """
        # if the candidate matches my regular expression
        if self.regexp.match(candidate):
            # indicate success
            return candidate
        # otherwise, fail
        raise self.ConstraintViolationError(self, candidate)


    # meta-methods
    def __init__(self, regexp, **kwds):
        # chain up
        super().__init__(**kwds)
        # compile my regular expression
        self.regexp = re.compile(regexp)
        # all done
        return


    def __str__(self):
        return "like {!r}".format(self.regexp.pattern)


# end of file 
