# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# unary expressions
class UnaryPostfix:
    """
    The base class for postfix unary expression factories
    """

    # public data
    operand = None
    operator = None


    # interface
    def sql(self):
        """SQL rendering of the expression I represent"""
        # straightforward
        return "{} {.operator}".format(self.operand.sql(), self)

    # meta-methods
    def __init__(self, operand, **kwds):
        # chain up
        super().__init__(**kwds)
        # store my value
        self.operand = operand
        # all done
        return


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
