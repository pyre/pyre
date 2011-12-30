# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


from ..algebraic import (
    AbstractNode, Number, Ordering, Boolean,
    Leaf, Composite,
    Literal, Variable, Operator
)


# class declaration
class Entry(AbstractNode, Number, Ordering, Boolean):
    """
    Base class for representing table fields and their algebra
    """


    # types
    # structural
    leaf = Leaf
    composite = Composite
    # functional; they will patched below with my subclasses
    literal = None
    variable = None
    operator = None


# literals
class literal(Entry, Literal, Entry.leaf):
    """
    Concrete class for representing foreign values
    """


# fields
class variable(Entry, Variable, Entry.leaf):
    """
    Concrete class for representing fields and their references
    """


# algebraic operations
class operator(Entry, Operator, Entry.composite):
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
