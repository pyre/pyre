# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# unary expressions
class UnaryPostfix:
    """
    The base class for postfix unary expression factories
    """

    # public data
    operand = None  # the expression the operator applies to
    operator = None  # and the operator, supplied by my subclasses

    # interface
    def sql(self):
        """
        SQL rendering of the expression I represent
        """
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


# some built-in functions
class Cast:
    """
    Implementation of the {CAST} expression
    """

    # interface
    def sql(self, **kwds):
        """
        SQL rendering of the expression I represent
        """
        # easy enough
        return "CAST({} AS {})".format(self.field.sql(**kwds), self.targetType.decl)

    # meta-methods
    def __init__(self, field, targetType, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my field reference
        self.field = field
        # and the target type
        self.targetType = targetType
        # all done
        return


# some built-in operators
class Like:
    """
    The match of a field against a pattern, in which a backslash escapes the wildcards
    """

    # public data
    escape = "\\"  # the character that escapes the wildcards in my pattern

    # meta-methods
    def __init__(self, field, pattern, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my field reference
        self.field = field
        # and the pattern
        self.pattern = pattern
        # all done
        return


# end of file
