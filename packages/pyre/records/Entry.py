# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# super classes
from ..schema.Descriptor import Descriptor
from ..algebraic.AbstractNode import AbstractNode
from ..algebraic.Number import Number

# my mix-ins
from .Field import Field
from .Derivation import Derivation
from .Literal import Literal


# declaration
class Entry(Descriptor, AbstractNode, Number):
    """
    The base class for record entries
    """


    # types
    # obligations from {pyre.algebraic} to support nodal algebra 
    # structural
    from ..algebraic.Leaf import Leaf as leaf
    from ..algebraic.Composite import Composite as composite

    # functional
    variable = None
    operator = None
    literal = None


    # public data
    aliases = None # the set of names by which I am accessible


    # interface
    def process(self, value):
        """
        Convert {value} into an object that is consistent with my type and value requirements
        """
        # cast it
        value = self.type.pyre_cast(value)
        # convert it
        for converter in self.converters:
            value = converter(value)
        # validate it
        for validator in self.validators:
            value = validator(value)
        # and return it
        return value

        
    # meta methods
    def __init__(self, aliases=None, **kwds):
        # chain to my ancestors
        super().__init__(**kwds)
        # initialize my aliases
        self.aliases = set() if aliases is None else aliases
        # all done
        return


# literals
class literal(Entry, Literal, Entry.leaf):
    """Concrete class for representing foreign values"""

class field(Entry, Field, Entry.leaf):
    """Concrete class for representing fields"""

class derivation(Entry, Derivation, Entry.composite):
    """Concrete class for representing derivations"""


# patch entry
Entry.literal = literal
Entry.variable = field
Entry.operator = derivation


# end of file 
