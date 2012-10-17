# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
from .. import algebraic


# class declaration
class Entry(algebraic.AbstractNode, algebraic.Arithmetic, algebraic.Ordering, algebraic.Boolean):
    """
    Base class for representing table fields and their algebra
    """


    # types
    # structural
    leaf = algebraic.Leaf
    composite = algebraic.Composite
    # functional; they will patched below with my subclasses
    literal = None
    variable = None
    operator = None


# literals
class literal(algebraic.Const, algebraic.Literal, Entry):
    """
    Concrete class for representing foreign values
    """


# fields
class variable(algebraic.Variable, Entry.leaf, Entry):
    """
    Concrete class for representing fields and their references
    """


# algebraic operations
class operator(algebraic.Operator, Entry.composite, Entry):
    """
    Concrete class for representing operations among fields and their references
    """

    # public data
    name = None # instances that appear in user code, e.g. query declarations, are named

    # meta methods
    def __str__(self):
        """Render my name"""
        return self.name


# patch {Entry}
Entry.literal = literal
Entry.variable = variable
Entry.operator = operator


# end of file 
