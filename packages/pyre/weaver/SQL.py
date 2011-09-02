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

        # access the {operator} module
        import operator
        # adjust the symbol table
        self._symbols[operator.pow] = "^"
        self._symbols[operator.eq] = "="
        self._symbols[operator.ne] = "<>"
        self._symbols[operator.abs] = "@"
        self._symbols[operator.and_] = "AND"
        self._symbols[operator.or_] = "OR"

        return


# end of file 
