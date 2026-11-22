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
class Cxx(LineMill, Expression):
    """
    Support for C++
    """

    # traits
    languageMarker = pyre.properties.str(default="C++")
    languageMarker.doc = "the variant to use in the language marker"

    # meta methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # adjust the symbol table: integer division is the division of integers
        self._symbols[operator.floordiv] = "/"
        # conjunction
        self._symbols[operator.and_] = "&&"
        # and disjunction use the operators of the language
        self._symbols[operator.or_] = "||"
        # and the rendering strategy table
        self._renderers[operator.pow] = self._powerRenderer
        # all done
        return

    # implementation details
    def _powerRenderer(self, node, **kwds):
        """
        Render the base of {node} raised to the power of its exponent
        """
        # get the base and the exponent
        base, exponent = node.operands
        # render the base
        op1 = self._render(node=base, **kwds)
        # and the exponent
        op2 = self._render(node=exponent, **kwds)
        # and hand them to the library function
        return f"pow({op1},{op2})"

    # private data
    comment = "//"


# end of file
