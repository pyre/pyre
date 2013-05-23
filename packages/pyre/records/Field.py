# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# declaration
class Field:
    """
    The base class for record entries
    """


    # types
    from ..calc.Node import Node as node


    # public data
    pyre_optional = False


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
            node = self.node.variable(value=self.coerce(value=next(stream)))
            # add it to the model
            model[self.name] = node
        # and return it
        return node


    def extract(self, stream, cache):
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
            value = self.coerce(value = next(stream))
            # cache it
            cache[self] = value

        # and return
        return value


    def __init__(self, optional=pyre_optional, **kwds):
        # chain up
        super().__init__(**kwds)
        # record whether this is an optional field, i.e. it may not be present in input sources
        self.pyre_optional = optional
        # all done
        return


# end of file 
