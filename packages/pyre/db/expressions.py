# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# unary expressions
class UnaryPostfix:
    """
    The base class for postfix unary expression factories
    """

    # public data
    operand = None
    operator = None

    # meta-methods
    def __init__(self, operand, **kwds):
        # chain up
        super().__init__(**kwds)
        # store my value
        self.operand = operand
        # all done
        return

    def __str__(self):
        return "{0.operand} {0.operator}".format(self)

    def __repr__(self): 
        return "{0.operand} {0.operator}".format(self)


class IsNull(UnaryPostfix):
    """
    A node factory that takes a field reference {op} and builds the expression {op IS NULL}
    """
    # public data
    operator = "IS NULL"


class IsNotNull(UnaryPostfix):
    """
    A node factory that takes a field reference {op} and builds the expression {op IS NOT NULL}
    """
    # public data
    operator = "IS NOT NULL"


# end of file
