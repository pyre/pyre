# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# superclass
from .. import algebraic


# declaration
class Calculator(algebraic.algebra):
    """
    Metaclass that grants nodes value management capabilities
    """


    # types
    from .Datum import Datum as base
    # entities: my literals, variables and operators have values
    from .Const import Const as const
    from .Value import Value as value
    from .Evaluator import Evaluator as evaluator
    # the new types of entities that support evaluation after name resolution
    from .Expression import Expression as expression
    from .Interpolation import Interpolation as interpolation
    from .Unresolved import Unresolved as unresolved
    # references to other nodes
    from .Reference import Reference as reference
    # local operators
    from .Average import Average as average
    from .Count import Count as count
    from .Maximum import Maximum as maximum
    from .Minimum import Minimum as minimum
    from .Product import Product as product
    from .Sum import Sum as sum
    # value change notification
    from .Observer import Observer as observer
    from .Observable import Observable as observable
    # value processing
    from .Preprocessor import Preprocessor as preprocessor
    from .Postprocessor import Postprocessor as postprocessor
    # value memoization
    from .Memo import Memo as memo
    # value filtering
    from .Filter import Filter as filter


    # meta-methods
    def __new__(cls, name, bases, attributes, ignore=False, **kwds):
        """
        Build a new class record
        """ 
        # build the record
        record = super().__new__(cls, name, bases, attributes, ignore=ignore, **kwds)
        # for specially marked classes, we are all done
        if ignore or cls.isIgnorable(bases): return record

        # the rest get some extra decoration: expressions, interpolations, and references
        # build the list of base classes for expression
        ancestors = tuple(cls.expressionDerivation(record))
        # make one
        record.expression = cls('expression', ancestors, {}, ignore=True)

        # build the list of base classes for interpolation
        ancestors = tuple(cls.interpolationDerivation(record))
        # make one
        record.interpolation = cls('interpolation', ancestors, {}, ignore=True)

        # build the list of base classes for reference
        ancestors = tuple(cls.referenceDerivation(record))
        # make one
        record.reference = cls('reference', ancestors, {}, ignore=True)

        # build the list of base classes for unresolved
        ancestors = tuple(cls.unresolvedDerivation(record))
        # make one
        record.unresolved = cls('unresolved', ancestors, {}, ignore=True)

        # build the list of base classes for average
        ancestors = tuple(cls.injectComposite(cls.average, record))
        # make one
        record.average = cls('average', ancestors, {}, ignore=True)
        
        # build the list of base classes for count
        ancestors = tuple(cls.injectComposite(cls.count, record))
        # make one
        record.count = cls('count', ancestors, {}, ignore=True)
        
        # build the list of base classes for max
        ancestors = tuple(cls.injectComposite(cls.maximum, record))
        # make one
        record.max = cls('max', ancestors, {}, ignore=True)
        
        # build the list of base classes for min
        ancestors = tuple(cls.injectComposite(cls.minimum, record))
        # make one
        record.min = cls('min', ancestors, {}, ignore=True)
        
        # build the list of base classes for product
        ancestors = tuple(cls.injectComposite(cls.product, record))
        # make one
        record.product = cls('product', ancestors, {}, ignore=True)
        
        # build the list of base classes for sum
        ancestors = tuple(cls.injectComposite(cls.sum, record))
        # make one
        record.sum = cls('sum', ancestors, {}, ignore=True)

        # all done
        return record


    # implementation details
    @classmethod
    def literalDerivation(cls, record):
        """
        Contribute to the list of ancestors of the representation of literals
        """
        # my literals have const values
        yield cls.const
        # and whatever else my superclass says
        yield from super().literalDerivation(record)
        # all done
        return


    @classmethod
    def variableDerivation(cls, record):
        """
        Contribute to the list of ancestors of the representation of literals
        """
        # my variable may reject invalid input
        yield cls.filter
        # my variables memoize their values
        yield cls.memo
        # my variables support arbitrary value conversions
        yield cls.preprocessor
        yield cls.postprocessor
        # my variables notify their clients of changes to their values
        yield cls.observable
        # my variables have values
        yield cls.value
        # and whatever else my superclass says
        yield from super().variableDerivation(record)
        # all done
        return


    @classmethod
    def operatorDerivation(cls, record):
        """
        Contribute to the list of ancestors of the representation of operators
        """
        # my operators memoize their values
        yield cls.memo
        # my operators support arbitrary value conversions
        yield cls.preprocessor
        yield cls.postprocessor
        # my operators notify their clients of changes to their values and respond when the
        # values of their operands change
        yield cls.observer
        # my operators know how to compute their values
        yield cls.evaluator
        # and whatever else my superclass says
        yield from super().operatorDerivation(record)
        # all done
        return


    @classmethod
    def expressionDerivation(cls, record):
        """
        Contribute to the list of ancestors of the representation of expressions
        """
        # my expressions memoize their values
        yield cls.memo
        # support arbitrary value conversions
        yield cls.preprocessor
        yield cls.postprocessor
        # notify their clients of changes to their values and respond when the values of their
        # operands change
        yield cls.observer
        # if the record has anything to say
        if record.expression: yield record.expression
        # this where they fit
        yield cls.expression
        # and whatever else my superclass says
        yield from cls.compositeDerivation(record)
        # all done
        return


    @classmethod
    def interpolationDerivation(cls, record):
        """
        Contribute to the list of ancestors of the representation of interpolations
        """
        # my interpolations memoize their values
        yield cls.memo
        # support arbitrary value conversions
        yield cls.preprocessor
        yield cls.postprocessor
        # notify their clients of changes to their values and respond when the values of their
        # operands change
        yield cls.observer
        # if the record has anything to say
        if record.interpolation: yield record.interpolation
        # this where they fit
        yield cls.interpolation
        # and whatever else my superclass says
        yield from cls.compositeDerivation(record)
        # all done
        return


    @classmethod
    def referenceDerivation(cls, record):
        """
        Contribute to the list of ancestors of the representation of references
        """
        # my references memoize their values
        yield cls.memo
        # support arbitrary value conversions
        yield cls.preprocessor
        yield cls.postprocessor
        # notify their clients of changes to their values and respond when the values of their
        # operands change
        yield cls.observer
        # if the record has anything to say
        if record.reference: yield record.reference
        # this where they fit
        yield cls.reference
        # and whatever else my superclass says
        yield from cls.compositeDerivation(record)
        # all done
        return


    @classmethod
    def unresolvedDerivation(cls, record):
        """
        Contribute to the list of ancestors of the representation of unresolved nodes
        """
        # my unresolved nodes notify their clients of changes to their values and respond when
        # the values of their operands change
        yield cls.observable
        # if the record has anything to say
        if record.unresolved: yield record.unresolved
        # my unresolved nodes know how to compute their values
        yield cls.unresolved
        # and whatever else my superclass says
        yield from cls.leafDerivation(record)
        # all done
        return


    @classmethod
    def injectComposite(cls, composite, record):
        """
        Place the class {composite} in the right spot in the {record} inheritance graph
        """
        # my local composites memoize their values
        yield cls.memo
        # support arbitrary value conversions
        yield cls.preprocessor
        yield cls.postprocessor
        # notify their clients of changes to their values and respond when the values of their
        # operands change
        yield cls.observer
        # this where they fit
        yield composite
        # and whatever else my superclass says
        yield from cls.compositeDerivation(record)
        # all done
        return


# end of file 
