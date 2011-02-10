# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# superclasses
from ..algebraic.Node import Node


# declaration
# it is important for this class not to derive from .Field: the item filters use isinstance to
# separate fields from derivations
class Derivation(Node):
    """
    This is the base class for all record items whose value depends on other items
    """


    # traversal of the nodes in my expression tree
    @property
    def pyre_dependencies(self):
        """
        Traverse my expression tree looking for leaf nodes
        """
        # just return myself
        return self.expression.pyre_dependencies


    # meta methods
    def __init__(self, expression, name=None, **kwds):
        super().__init__(**kwds)
        self.name = None
        self.expression = expression
        return


    # interface
    def pyre_recordFieldAccessor(self, record, index):
        """
        Ask {record} for an accessor factory that it appropriate for derivations and use it to
        build one that knows my index in the tuple of items of {record} 
        """
        return record.pyre_derivationAccessor(index=index, field=self)


    def pyre_patch(self, replacements):
        """
        Look through the dictionary {replacements} for any of my operands and replace them with
        the indicated nodes.
        """
        # patch my expression
        self.expression.pyre_patch(replacements)
        # and return
        return


    def eval(self, *, cache, **kwds):
        """
        Compute and return the value of my expression
        """
        # check whether I have done this before
        if self in cache:
            # yes; return the previously computed value
            return cache[self]
        # nope; compute and return the value of my expression
        return self.expression.eval(cache=cache)
        

# end of file 
