# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# my mix-ins
from .Typed import Typed
from .Public import Public
from .Default import Default

# to get my algebra
from .. import algebraic


# declaration
class Descriptor(algebraic.AbstractNode,
                 algebraic.Arithmetic, algebraic.Ordering, algebraic.Boolean):
    """
    The base class for typed descriptors

    Descriptors are class data members that collect compile time meta-data about attributes.

    In pyre, classes that use descriptors typically have a non-trivial metaclass that harvests
    them and catalogs them. The base class that implements most of the harvesting logic is
    {pyre.patterns.AttributeClassifier}. The descriptors themselves are typically typed,
    because they play some kind of rôle during conversions between internal and external
    representations of data.
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


    # interface
    def attach(self, **kwds):
        """
        Called by my client to let me know that all the available meta-data have been harvested
        """
        # end of the line; nothing else to do
        return self



# variables
class descriptor(Typed, Public, Default, algebraic.Variable, Descriptor.leaf, Descriptor):
    """Concrete class for representing fields"""

# representations of the various operations among descriptors
class operator(Typed, Public, algebraic.Operator, Descriptor.composite, Descriptor):
    """Concrete class for representing derivations"""

# literals, to close the algebra
class literal(Typed, algebraic.Const, algebraic.Literal, Descriptor):
    """Concrete class for representing foreign values"""


# patch entry
Descriptor.literal = literal
Descriptor.variable = descriptor
Descriptor.operator = operator


# end of file 
