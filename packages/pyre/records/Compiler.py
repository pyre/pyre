# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# declaration
class Compiler:
    """
    A strategy for pulling data from a stream and building {pyre.calc} nodes to represent both
    measures and derivations
    """

    # types
    from ..calc.Node import Node as node

    # interface
    def arity(self, record) -> int:
        """
        The number of values a row of {record} holds: one for each of its measures, since its
        derivations are computed
        """
        # easy enough
        return len(record.pyre_measures)

    # meta-methods
    def __call__(self, record, source, **kwds):
        """
        Pull the values of the measures of {record} from {source}, and build the nodes of its
        fields
        """
        # make {pyre.calc} variables so the measures are mutable
        variable = self.node.variable
        # the row holds the values of the measures, in the order of the layout; make a node for
        # each, and keep them where the derivations can find them
        cache = {
            measure: variable(value=value, postprocessor=measure.process)
            for measure, value in zip(record.pyre_measures, source)
        }
        # the fields the record shadows stand for the fields that replace them
        shadows = record.pyre_shadows
        # go through the fields of the record
        for field in record.pyre_fields:
            # ask each one to dispatch to its handler, which knows how to find its node
            node = field.identify(authority=self, cache=cache, shadows=shadows)
            # and make the node available
            yield node
        # all done
        return

    # implementation details
    def onDescriptor(self, descriptor, cache, shadows, **kwds):
        """
        Handler for measures
        """
        # a measure the record shadows
        replacement = shadows.get(descriptor)
        # stands for the field that replaces it
        if replacement is not None:
            # whose node is the one we want
            return replacement.identify(authority=self, cache=cache, shadows=shadows)
        # every other measure has its node from the row
        return cache[descriptor]

    def onOperator(self, operator, cache, shadows, **kwds):
        """
        Handler for derivations
        """
        # a derivation the record shadows
        replacement = shadows.get(operator)
        # stands for the field that replaces it
        if replacement is not None:
            # whose node is the one we want
            return replacement.identify(authority=self, cache=cache, shadows=shadows)
        # if the node of this {operator} is built already
        try:
            # use it
            return cache[operator]
        # if not
        except KeyError:
            # build it
            pass
        # find the nodes of its operands
        operands = tuple(
            operand.identify(authority=self, cache=cache, shadows=shadows)
            for operand in operator.operands
        )
        # make an operator node
        node = self.node.operator(
            evaluator=operator.evaluator, postprocessor=operator.process, operands=operands
        )
        # remember it, since other derivations may use it
        cache[operator] = node
        # and make it available
        return node

    def onLiteral(self, literal, **kwds):
        """
        Handler for literals
        """
        # build a literal node with the same value as the foreign object
        return self.node.literal(value=literal._value)


# end of file
