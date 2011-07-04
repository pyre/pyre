# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


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
    languageMarker = pyre.properties.str(default='C++')
    languageMarker.doc = "the variant to use in the language marker"

    
    # meta methods
    def __init__(self, **kwds):
        super().__init__(comment='//', **kwds)

        # adjust the symbol table
        self._symbols[self.algebraic.And] = "&&"
        self._symbols[self.algebraic.Or] = "||"

        # and the rendering strategy table
        self._renderers[self.algebraic.Power] = self._powerRenderer

        return


    # implementation details
    def _powerRenderer(self, node):
        """
        Render {node.op1} raised to the {node.op2} power
        """
        # render my operands
        op1 = self._renderers[node.op1.__class__](node.op1)
        op2 = self._renderers[node.op2.__class__](node.op2)
        # and return my string
        return "pow({},{})".format(op1, op2)


# end of file 
