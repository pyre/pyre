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
class SQL(LineMill, Expression):
    """
    Support for SQL
    """


    # traits
    languageMarker = pyre.properties.str(default='SQL')
    languageMarker.doc = "the variant to use in the language marker"

    
    # meta methods
    def __init__(self, **kwds):
        super().__init__(comment='--', **kwds)

        # adjust the symbol table
        self._symbols[self.algebraic.And] = "AND"
        self._symbols[self.algebraic.Equal] = "="
        self._symbols[self.algebraic.NotEqual] = "<>"
        self._symbols[self.algebraic.Or] = "OR"
        self._symbols[self.algebraic.Power] = "^"

        return


    def _absoluteRenderer(self, node):
        """
        Render the absolute value of {node}
        """
        # render my operand
        op = self._renderers[node.op.__class__](node.op)
        # and return my string
        return "@({})".format(op)
        

# end of file 
