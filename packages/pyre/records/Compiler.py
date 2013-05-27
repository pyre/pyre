# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


class Compiler:
    """
    A strategy for pulling data from a stream and building {pyre.calc} nodes to represent both
    measures and derivations
    """


    # types
    from ..calc.Node import Node as node


    # meta-methods
    def __call__(self, record, source, **kwds):
        """
        Pull values from {source} and build the associated nodes
        """
        # build a cache
        cache = {}
        # go through the entries in {record}
        for entry in record.pyre_entries:
            # ask each one to dispatch to the appropriate handler to build the node
            node = entry.identify(authority=self, cache=cache, source=source)
            # update the cache
            cache[entry] = node
            # and make the node available
            yield node
        # all done
        return


    # implementation details
    def onDescriptor(self, source, cache, descriptor):
        """
        Handler for measures
        """
        # if i have been asked for the value of this {descriptor} before
        try:
            # get it
            node = cache[descriptor]
        # if not
        except KeyError:
            # grab one from the data stream
            value = next(source)
            # build a node for it
            node = self.node.variable(value=value, converter=descriptor.coerce)
        # and make it available
        return node


    def onOperator(self, source, cache, descriptor):
        """
        Handler for derivations
        """
        # if I have visited this descriptor before
        try:
            # get the previously built node
            node = cache[descriptor]
        # if not
        except KeyError:
            # build a node for its operands
            operands = tuple(
                # by processing
                op.identify(authority=self, cache=cache, source=source)
                # each operand
                for op in descriptor.operands)
            # make an operator node
            node = self.node.operator(
                evaluator=descriptor.evaluator, converter=descriptor.coerce, operands=operands)
        # and make it available
        return node


    def onLiteral(self, source, cache, descriptor):
        """
        Handler for literals
        """
        # just return the descriptor itself; is there ever a need to build a new one?
        return descriptor


# end of file
