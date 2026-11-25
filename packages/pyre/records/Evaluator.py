# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# declaration
class Evaluator:
    """
    A strategy for pulling data from a stream, and performing evaluations and coercions as
    indicated by the field descriptors
    """

    # interface
    def arity(self, record) -> int:
        """
        The number of values a row of {record} holds: one for each of its measures, since its
        derivations are computed
        """
        # easy enough
        return len(record.pyre_measures)

    # meta methods
    def __call__(self, record, source, **kwds):
        """
        Pull the values of the measures of {record} from {source}, compute its derivations, walk
        every value through its coercions, and make the results available to the caller
        """
        # the row holds the values of the measures, in the order of the layout; convert them, and
        # keep them where the derivations can find them
        cache = {
            measure: measure.process(value) for measure, value in zip(record.pyre_measures, source)
        }
        # the fields the record shadows stand for the fields that replace them
        shadows = record.pyre_shadows
        # go through the fields of the record
        for field in record.pyre_fields:
            # and ask each one to dispatch to its handler, which knows how to find its value
            value = field.identify(authority=self, cache=cache, shadows=shadows)
            # make the value available
            yield value
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
            # whose value is the one we want
            return replacement.identify(authority=self, cache=cache, shadows=shadows)
        # every other measure has its value from the row
        return cache[descriptor]

    def onOperator(self, operator, cache, shadows, **kwds):
        """
        Handler for operators
        """
        # a derivation the record shadows
        replacement = shadows.get(operator)
        # stands for the field that replaces it
        if replacement is not None:
            # whose value is the one we want
            return replacement.identify(authority=self, cache=cache, shadows=shadows)
        # if the value of this {operator} is known already
        try:
            # use it
            return cache[operator]
        # if not
        except KeyError:
            # compute it
            pass
        # find the values of its operands
        values = tuple(
            operand.identify(authority=self, cache=cache, shadows=shadows)
            for operand in operator.operands
        )
        # apply its evaluator to them, and coerce the result
        value = operator.process(operator.evaluator(*values))
        # remember it, since other derivations may use it
        cache[operator] = value
        # and make it available
        return value

    def onLiteral(self, literal, **kwds):
        """
        Handler for descriptors that encapsulate foreign values
        """
        # ask it for its value
        return literal._value


# end of file
