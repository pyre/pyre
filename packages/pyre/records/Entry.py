# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# super classes
from .. import algebraic
from ..traits.Descriptor import Descriptor

# my mix-ins
from .Field import Field
from .Derivation import Derivation
from .Literal import Literal


# declaration
class Entry(Descriptor, algebraic.AbstractNode, algebraic.Arithmetic):
    """
    The base class for record entries
    """


    # types
    # obligations from {pyre.algebraic} to support nodal algebra 
    # structural
    leaf = algebraic.Leaf
    composite = algebraic.Composite

    # functional
    literal = None
    variable = None
    operator = None


    # public data
    validators = () # the chain of functions that inspect and validate my value
    converters = () # the chain of transformations necessary to produce a value in my native type


    # interface
    def process(self, value):
        """
        Convert {value} into an object that is consistent with my type and value requirements
        """
        # cast it
        value = self.schema.coerce(value)
        # convert it
        for converter in self.converters:
            value = converter(value)
        # validate it
        for validator in self.validators:
            value = validator(value)
        # and return it
        return value

        
# literals
class literal(Literal, algebraic.Const, algebraic.Literal, Entry):
    """Concrete class for representing foreign values"""

class field(Field, algebraic.Variable, Entry.leaf, Entry):
    """Concrete class for representing fields"""

class derivation(Derivation, algebraic.Operator, Entry.composite, Entry):
    """Concrete class for representing derivations"""


# patch entry
Entry.literal = literal
Entry.variable = field
Entry.operator = derivation


# end of file 
