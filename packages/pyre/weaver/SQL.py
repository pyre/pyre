# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import operator

# access to the pyre package
import pyre

# my ancestors
from .LineMill import LineMill
from .Expression import Expression


# my declaration
class SQL(LineMill, Expression):
    """
    Support for SQL
    """

    # traits
    languageMarker = pyre.properties.str(default="SQL")
    languageMarker.doc = "the variant to use in the language marker"

    # meta methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)

        # adjust the symbol table: exponentiation is a function
        self._symbols[operator.pow] = "POWER"
        # and so are the remainder
        self._symbols[operator.mod] = "MOD"
        # and the absolute value
        self._symbols[operator.abs] = "ABS"
        # there is no floor division, so it takes the floor of the quotient
        self._symbols[operator.floordiv] = "FLOOR"
        # equality
        self._symbols[operator.eq] = "="
        # inequality
        self._symbols[operator.ne] = "<>"
        # the logical operators are spelled out
        self._symbols[operator.and_] = "AND"
        # all of them
        self._symbols[operator.or_] = "OR"

        # the functions render as calls: exponentiation
        self._renderers[operator.pow] = self._functionRenderer
        # the remainder
        self._renderers[operator.mod] = self._functionRenderer
        # and the absolute value
        self._renderers[operator.abs] = self._functionRenderer
        # floor division has a renderer of its own
        self._renderers[operator.floordiv] = self._floorDivisionRenderer
        # all done
        return

    # implementation details
    def _functionRenderer(self, node, **kwds):
        """
        Render {node} as a call to the function its operator stands for
        """
        # render the arguments
        arguments = (
            self._renderers[type(operand)](node=operand, **kwds) for operand in node.operands
        )
        # look up the name of the function
        function = self._symbols[node.evaluator]
        # and put it all together
        return f"{function}({', '.join(arguments)})"

    def _floorDivisionRenderer(self, node, **kwds):
        """
        Render {node} as the floor of the quotient of its operands; the division of two integers
        truncates toward zero before the floor is taken
        """
        # extract the operands
        dividend, divisor = node.operands
        # render the dividend
        numerator = self._renderers[type(dividend)](node=dividend, **kwds)
        # and the divisor
        denominator = self._renderers[type(divisor)](node=divisor, **kwds)
        # look up the name of the function that takes the floor
        floor = self._symbols[node.evaluator]
        # and the symbol of the division
        quotient = self._symbols[operator.truediv]
        # put it all together
        return f"{floor}(({numerator}) {quotient} ({denominator}))"

    # overrides
    def _literalRenderer(self, node, **kwds):
        """
        Render {node} as a literal
        """
        # get the value of the node
        value = node._value
        # if it is already a string
        if isinstance(value, str):
            # just escape the single quotes
            escaped = value.replace("'", "''")
            # and quote it
            return f"'{escaped}'"

        # check whether
        try:
            # it knows how to render itself
            rendering = value.sql()
        # otherwise
        except AttributeError:
            # last resort: render the value as a string
            rendering = str(value)
        # either way, return the {rendering}
        return rendering

    # private data
    comment = "--"


# end of file
