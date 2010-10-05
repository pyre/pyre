# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from . import _metaclass_Node
from ..patterns.Observable import Observable


class Node(Observable, metaclass=_metaclass_Node):
    """
    Base class for objects in evaluation graphs
    """


    # access to the evaluator base
    from .Evaluator import Evaluator
    # and some evaluator factories
    from .Literal import Literal
    from .Reference import Reference


    # interface
    def getValue(self):
        """
        Refresh my value, if necessary, and return it
        """
        # if my cached value is invalid
        if self._value is None:
            # get my evaluator to refresh it
            try:
                self._value = self._evaluator and self._evaluator.compute()
            # leave unresolved node errors alone
            except self.UnresolvedNodeError as error:
                error.node = self
                raise
            # dress anything else up as an EvaluationError
            except Exception as error:
                raise self.EvaluationError(evaluator=self, error=error) from error
        # and return it
        return self._value


    def setValue(self, value):
        """
        Set my value to {value} and notify my observers
        """
        # invalidate my cache
        self._value = None
        # if i already have an evaluator
        if self._evaluator is not None:
            # clear it out
            self._evaluator.finalize(owner=self)
        # build my new evaluator
        if isinstance(value, self.Evaluator):
            evaluator = value
        else:
            evaluator = self.Literal(value=value)
        # initialize it
        evaluator.initialize(owner=self)
        # attach it
        self._evaluator = evaluator
        # invalidate my observers' caches
        self.notifyObservers()
        # and return
        return self


    # install value setter/getter as a property
    value = property(fget=getValue, fset=setValue, fdel=None, doc="Access to my value")


    # interface
    def merge(self, other):
        """
        Transfer the information from {other} if its priority is higher or equal to mine
        """
        # print("pyre.calc.Node.merge:")
        # print(" ++ this:")
        # self.dump()
        # print(" ++ other:")
        # other.dump()
        # invalidate my cache
        self._value = None
        # grab stuff from other
        value = other._value
        evaluator = other._evaluator
        # shutdown my evaluator
        if self._evaluator:  self._evaluator.finalize(owner=self)
        # if other had an evaluator
        if evaluator: 
            # shut it down
            evaluator.finalize(owner=other)
            # initialize it for me
            evaluator.initialize(owner=self)
        # otherwise
        else:
            # build a literal out of the other's value
            # literals don't need to be initialized
            evaluator = None if value is None else self.Literal(value=other._value)
        # atatch the evaluator to me
        self._evaluator = evaluator

        # update the my observers
        self.observers.update(other.observers)
        # notify the old observers of the change
        for observer in other.observers:
            # domain adjustments
            observer.patch(new=self, old=other)

        # notify my observers
        self.notifyObservers()

        # print(" ++ after the merge:")
        # self.dump()
        # and return
        return

        
    def validate(self, span=None, clean=None):
        """
        Make sure that my branch of the evaluation graph is free of cycles

        parameters:
            {span}: the set of nodes previously visited; if i am in this set, there are cycles
            {clean}: the set of nodes known to be cycle free because they were previously cleared
       """
        # initialize my optional parameters
        span = set() if span is None else span
        clean = set() if clean is None else clean
        # if i am in the span, we have a cycle
        if self in span:
            raise self.CircularReferenceError(node=self, path=span)
        # if i have an evaluator, visit all the nodes in its domain
        if self._evaluator:
            # add me to the current span
            span.add(self)
            # get the evaluator to loop over its domain
            self._evaluator.validate(span, clean)
        # if i made it this far without an exception, i must be clean
        # so add myself to the clean pile
        clean.add(self)
        # and return
        return self


    def flush(self, node=None):
        """
        Invalidate my cache and notify my observers
        """
        # if my value is already invalid, there is nothing to do
        if self._value is None: return
        # otherwise, invalidate my cache
        self._value = None
        # notify the observers
        self.notifyObservers()
        # and return
        return self


    def patch(self, new, old):
        """
        Stop watching {old} and start monitoring {new}

        This is here only because there can be many different kinds of nodes in an evaluation
        graph, many of which may have non-standard storage strategies for their
        observables. The class Probe in this package is such an example.
        """
        # flush me
        self.flush()
        # if i don't have an evaluator, this is a bug
        return self._evaluator.patch(old=old, new=new)


    # evaluator factories
    @classmethod
    def newLiteral(cls, value, **kwds):
        """
        Build a new literal evaluator
        """
        return cls.Literal(value=value, **kwds)


    def newReference(self, **kwds):
        """
        Build a new reference to me
        """
        return self.Reference(node=self)
        

    # exceptions
    from .exceptions import CircularReferenceError, EvaluationError, UnresolvedNodeError


    # my algebra
    def __add__(self, other):
        if isinstance(other, Node):
            from .Addition import Addition
            return Node(value=None, evaluator=Addition(op1=self, op2=other))
                    
        from .Increment import Increment
        return Node(value=None, evaluator=Increment(node=self, increment=other))

        
    def __mul__(self, other):
        if isinstance(other, Node):
            from .Multiplication import Multiplication
            return Node(value=None, evaluator=Multiplication(op1=self, op2=other))

        from .Scaling import Scaling
        return Node(value=None, evaluator=Scaling(node=self, factor=other))
                    
        
    def __sub__(self, other):
        if isinstance(other, Node):
            from .Subtraction import Subtraction
            return Node(value=None, evaluator=Subtraction(op1=self, op2=other))
                    
        from .Increment import Increment
        return Node(value=None, evaluator=Increment(node=self, increment=-other))

        
    def __truediv__(self, other):
        if isinstance(other, Node):
            from .Division import Division
            return Node(value=None, evaluator=Division(op1=self, op2=other))

        from .Scaling import Scaling
        return Node(value=None, evaluator=Scaling(node=self, factor=1/other))
                    
        
    def __rmul__(self, scalar):
        from .Scaling import Scaling
        return Node(value=None, evaluator=Scaling(node=self, factor=scalar))
                    

    # meta methods
    def __init__(self, value, evaluator, **kwds):
        """
        Unless you are building a {Node} specialization, it is almost always better to use the
        factory methods provided in the pyre.calc package, rather than calling this constructor
        directly
        """
        super().__init__(**kwds)
        self._value = value
        self._evaluator = evaluator and evaluator.initialize(owner=self)
        return


    # debugging
    def dump(self, tag=None):
        """
        Debugging tool that print out the relevant parts
        """
        tag = tag + ": " if tag else ''

        print("{}{}".format(tag, self))
        print("   value: {}".format(self._value))
        print("   evaluator: {}".format(self._evaluator))

        if self._evaluator:
            for idx,op in enumerate(self._evaluator.domain):
                print("       op {}: {}".format(idx, op))

        if self.observers:
            print("   observers:")
            for idx, observer in enumerate(self.observers):
                print("       {}: {}".format(idx, observer))

        return


    # private data
    _value = None
    _evaluator = None


# end of file 
