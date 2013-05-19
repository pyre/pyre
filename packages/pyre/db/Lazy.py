# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# the node structure
from .. import algebraic


# declaration of the base class
class Lazy(algebraic.AbstractNode, algebraic.Arithmetic):
    """
    The base class for lazily computed record values
    """


    # types: hooks for implementing the expression graph construction
    # the mix-ins
    leaf = algebraic.Leaf
    literal = algebraic.Literal
    composite = algebraic.Composite
    const = algebraic.Const
    memo = algebraic.Memo
    observer = algebraic.Observer
    observable = algebraic.Observable
    # the functionals; they will be patched below with my subclasses
    variable = None
    operator = None
    reference = None
    counter = None


    # meta-methods
    def __str__(self):
        # invoked during the construction of the SQL statement
        return self.value


    def __repr__(self):
        # invoked during the construction of the SQL statement
        return self.value


# literals
class literal(Lazy.const, Lazy.literal, Lazy):
    """
    Concrete class for representing foreign values
    """

# variables
class variable(Lazy.observable, algebraic.Variable, Lazy.leaf, Lazy):
    """
    Concrete class for encapsulating the user accessible nodes
    """

# operators
class operator(Lazy.memo, Lazy.observer, algebraic.Operator, Lazy.composite, Lazy):
    """
    Concrete class for encapsulating operations among nodes
    """

# references
class reference(Lazy.observer, algebraic.Reference, Lazy.composite, Lazy):
    """
    Concrete class for encapsulating references to other nodes
    """

    # meta-methods
    def __init__(self, node, **kwds):
        # chain up
        super().__init__(operands=(node,), **kwds)
        # all done
        return

# counters
class counter(Lazy.observable, Lazy.leaf, Lazy):
    """
    Class that gets its value by poking an iterator
    """

    # interface
    def getValue(self):
        """
        Return my value
        """
        raise NotImplementedError("hell")
        # if i haven't been evaluate before
        if self._value is None: 
            # get a value by asking my counter for one
            self._value = next(self._counter)
        # return my value
        return self._value

    def setValue(self, value):
        """
        Disable value setting
        """
        # disabled
        raise NotImplementedError("counters do not support 'setValue'")

    # meta methods
    def __init__(self, counter, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my counter
        self._counter = counter
        # mark my value as unknown
        self._value = None
        # all done
        return


# patch the base class
Lazy.literal = literal
Lazy.variable = variable
Lazy.operator = operator
Lazy.reference = reference
Lazy.counter = counter


# end of file 
