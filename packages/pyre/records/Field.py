# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# declaration
class Field:
    """
    The base class for record entries
    """


    # types
    from ..calc.Node import Node as node


    # interface
    def buildNode(self, stream, model):
        """
        Extract a value from {stream} and use it to build a {pyre.calc} node 
        """
        # have we done this before?
        try:
            # just return the previous node 
            node = model[self.name]
        # if not
        except KeyError:
            # make the node
            node = self.node.variable(value=self.extract(stream))
            # add it to the model
            model[self.name] = node
        # and return it
        return node


    def extract(self, stream):
        """
        Extract a value from {stream} and walk it through casting, conversion and validation.
        """
        # get the value from the {stream}, process it and return it
        return self.process(value=next(stream))


    def evaluate(self, stream, cache):
        """
        Compute my value by either returning a previous evaluation or by extracting an item
        from {stream} and processing it
        """
        # if I have computed my value before
        try:
            # retrieve it it
            value = cache[self]
        # otherwise
        except KeyError:
            # compute it
            value = self.extract(stream=stream)
            # cache it
            cache[self] = value

        # and return
        return value


# end of file 
