# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# superclasses
from .Entry import Entry
from ..algebraic.Composite import Composite


# declaration
class Derivation(Composite, Entry):
    """
    The base class for record entries whose values are computed using other record fields
    """


    # types
    from ..calc.Operator import Operator as node


    # interface
    def buildNode(self, stream, model):
        """
        Build a {pyre.calc} node over my operands
        """
        # have we done this before?
        try:
            # just return the previous node 
            node = model[self.name]
        # if not
        except KeyError:
            # make a node for each of my operands
            operands = tuple(op.buildNode(stream, model) for op in self.operands)
            # make a node for myself
            node = self.node(evaluator=self.evaluator, operands=operands)
            # if I am a named node, i.e. one that shows up in a record declaration
            if self.name is not None:
                # add my node to the model
                model[self.name] = node
        # and return the new node
        return node


    def evaluate(self, stream, cache):
        """
        Compute my value by either returning a previous evaluation or by extracting an item
        from {stream} and processing it
        """
        # if i have computed my value before
        try:
            # retrieve it it
            value = cache[self]
        # otherwise
        except KeyError:
            # compute the values of my operands
            values = tuple(op.evaluate(stream, cache) for op in self.operands)
            # apply my operator
            value = self.evaluator(*values)
            # cache it
            cache[self] = value

        # and return
        return value

        
    # meta methods
    def __init__(self, evaluator, operands, **kwds):
        super().__init__(**kwds)
        self.evaluator = evaluator
        self.operands = operands
        return



# end of file 
