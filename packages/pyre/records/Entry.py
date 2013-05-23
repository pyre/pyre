# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# super classes
from .. import algebraic
from ..schemata import descriptor

# my mix-ins
from .Field import Field
from .Derivation import Derivation
from .Literal import Literal


# declaration
class Entry(descriptor, algebraic.AbstractNode, algebraic.Arithmetic):
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
