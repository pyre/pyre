# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# superclasses
from ..algebraic.Node import Node


# declaration
class FieldProxy(Node):
    """
    Replacements for actual {Field} nodes in expressions that involve them.

    The job of {FieldProxy} is to ensure that fields are not evaluated more than once.
    """


    # interface
    def pyre_eval(self, *, cache, **kwds):
        """
        Look up and return the value of my field
        """
        # return the previously computed value
        return cache[self.field]


    # meta methods
    def __init__(self, field, **kwds):
        # chain to the ancestors
        super().__init__(**kwds)
        # save my field
        self.field = field
        # all done
        return


# end of file 
