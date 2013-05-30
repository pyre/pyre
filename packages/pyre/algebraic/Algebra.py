# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# superclass
from .Category import Category


# declaration
class Algebra(Category):
    """
    Metaclass that endows its instances with algebraic structure
    """


    # types
    from .AbstractNode import AbstractNode as base
    # algebraic
    from .Arithmetic import Arithmetic as arithmetic
    from .Ordering import Ordering as ordering
    from .Boolean import Boolean as boolean
    # structural
    from .Leaf import Leaf as leaf
    from .Composite import Composite as composite
    # entities
    from .Literal import Literal as literal
    from .Variable import Variable as variable
    from .Operator import Operator as operator


    # meta-methods
    def __new__(cls, name, bases, attributes, 
                arithmetic=True, ordering=True, boolean=True, 
                ignore=False,
                **kwds):
        """
        Build a new class record
        """ 
        # go through each of the bases
        for base in bases:
            # looking for
            try:
                # a marked one
                base._hasAlgebra
            # of that fails
            except AttributeError:
                # no problem, skip it
                continue
            # otherwise
            else:
                # this class derived from one of mine, so skip it
                return super().__new__(cls, name, bases, attributes, **kwds)
        
        # skip explicitly marked classes
        if ignore: return super().__new__(cls, name, bases, attributes, **kwds)

        # prime the list of ancestors
        ancestors = [cls.base]
        # if we were asked to support arithmetic, add support for it
        if arithmetic: ancestors.append(cls.arithmetic)
        # if we were asked to support ordering, add support for it
        if ordering: ancestors.append(cls.ordering)
        # if we were asked to support boolean operations, add support for it
        if boolean: ancestors.append(cls.boolean)
        # wrap up by piling on the actual bases of the client
        bases = tuple(ancestors) + bases

        # build the record
        record = super().__new__(cls, name, bases, attributes, **kwds)

        # build the list of base classes for the literal
        ancestors = tuple(cls.literalDerivation(record))
        # make one
        record.literal = cls('literal', ancestors, {}, ignore=True)

        # build the list of base classes for the variable
        ancestors = tuple(cls.variableDerivation(record))
        # make one
        record.variable = cls('variable', ancestors, {}, ignore=True)

        # build the list of base classes for operators
        ancestors = tuple(cls.operatorDerivation(record))
        # make one
        record.operator = cls('operator', ancestors, {}, ignore=True)

        # mark it
        record._hasAlgebra = True

        # return the record
        return record


    # implementation details
    @classmethod
    def literalDerivation(cls, record):
        """
        Contribute to the list of ancestors of the representation of literals
        """
        # if the class record specifies a literal mix-in use it, otherwise use the default
        yield record.literal if record.literal else cls.literal
        # get the classes necessary to make leaves
        yield from cls.leafDerivation(record)
        # all done
        return


    @classmethod
    def variableDerivation(cls, record):
        """
        Contribute to the list of ancestors of the representation of variables
        """
        # if the class record specifies a variable mix-in use it
        if record.variable: yield record.variable
        # must also derive from the default
        yield cls.variable
        # get the classes necessary to make leaves
        yield from cls.leafDerivation(record)
        # all done
        return


    @classmethod
    def operatorDerivation(cls, record):
        """
        Contribute to the list of ancestors of the representation of operators
        """
        # if the class record specifies a operator mix-in use it
        if record.operator: yield record.operator 
        # must also derive from the default
        yield cls.operator
        # get the classes necessary to make composites
        yield from cls.compositeDerivation(record)
        # all done
        return


# end of file 
