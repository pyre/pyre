# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
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
    converters = () # the chain of transformations necessary to produce a value in my native type
    normalizers = () # the chain of transformations that convert my value to normal form
    validators = () # the chain of functions that inspect and validate my value


    # interface
    def process(self, value):
        """
        Convert {value} into an object that is consistent with my type and value requirements
        """
        # convert it
        for converter in self.converters:
            value = converter(value)
        # cast it
        value = self.schema.coerce(value)
        # normalize it
        for normalizer in self.normalizers:
            value = normalizer(value)
        # validate it
        for validator in self.validators:
            value = validator(value)
        # and return it
        return value


    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # reset my data processors
        self.converters = []
        self.normalizers = []
        self.validators = []
        # all done
        return

        
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
