# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# unary expressions
class UnaryPostfix:
    """
    The base class of the expressions that apply an operator to the operand that precedes it
    """

    # public data
    operand = None  # the expression the operator applies to

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
    The test of whether the field reference {operand} is {NULL}
    """

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a test of whether my operand is {NULL}
        """
        # ask for my handler
        return authority._pyre_onIsNull(node=self, **kwds)


class IsNotNull(UnaryPostfix):
    """
    The test of whether the field reference {operand} is anything but {NULL}
    """

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a test of whether my operand is anything but {NULL}
        """
        # ask for my handler
        return authority._pyre_onIsNotNull(node=self, **kwds)


# some built-in functions
class Cast:
    """
    The conversion of the value of a field to another type
    """

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a conversion
        """
        # ask for my handler
        return authority._pyre_onCast(node=self, **kwds)

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

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am the match of a field against a pattern
        """
        # ask for my handler
        return authority._pyre_onLike(node=self, **kwds)

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
