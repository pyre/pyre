# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the nodes of the algebra of the fields
from ... import descriptors


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


# the negation of a predicate
class Negation:
    """
    The negation of the predicate {predicate}
    """

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am the negation of a predicate
        """
        # ask for my handler
        return authority._pyre_onNegation(node=self, **kwds)

    # meta-methods
    def __init__(self, predicate, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the predicate i negate
        self.predicate = predicate
        # all done
        return


# membership
class IsIn:
    """
    The test of whether the field reference {field} holds one of {values}
    """

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a test of membership
        """
        # ask for my handler
        return authority._pyre_onIsIn(node=self, **kwds)

    # meta-methods
    def __init__(self, field, values, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my field reference
        self.field = field
        # and the values, in their order
        self.values = tuple(values)
        # all done
        return


# some built-in functions
class Cast(descriptors.stem.operator):
    """
    The conversion of the value of a field to another type

    A cast is a node of the algebra of the fields: its one operand is the field, its evaluator
    converts a value to the target type, and it takes part in projections and comparisons like
    any other expression
    """

    # interface
    def coerce(self, value, **kwds):
        """
        Convert {value} to my target type
        """
        # my target type knows
        return self.targetType.coerce(value=value, **kwds)

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a conversion
        """
        # ask for my handler
        return authority._pyre_onCast(node=self, **kwds)

    # meta-methods
    def __init__(self, field, targetType, **kwds):
        # chain up, with the field as my one operand and the conversion as my evaluator
        super().__init__(evaluator=targetType.coerce, operands=(field,), **kwds)
        # save the target type
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
