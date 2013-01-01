# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


from .Constraint import Constraint


class Like(Constraint):
    """
    Given a regular expression, a string satisfies this constraint if it matches the regular
    expression
    """


    def validate(self, candidate):
        if self.regexp.match(candidate):
            return candidate

        raise self.ConstraintViolationError(self, candidate)


    def __init__(self, regexp, **kwds):
        import re

        super().__init__(**kwds)

        self.regexp = re.compile(regexp)
        return


    def __str__(self):
        return "like {0!r}".format(self.regexp.pattern)


# end of file 
