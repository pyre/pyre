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


    # access to commonly used evaluators
    from .Evaluator import Evaluator
    from .Expression import Expression
    from .Literal import Literal
    from .Reference import Reference


    # public data
    @property
    def value(self):
        """
        Refresh my value, if necessary, and return it
        """
        return self._getValue()


    @value.setter
    def value(self, value):
        """
        Set my value to the passed literal value and notify my observers

        This implies that i do not need my evaluator any more, so it is destroyed
        """
        return self._setValue(value)


    @property
    def evaluator(self):
        """
        Get my evaluator
        """
        return self._evaluator


    @evaluator.setter
    def evaluator(self, evaluator):
        """
        Install a new evaluator
        """
        return self._setEvaluator(evaluator)


    # introspection and evaluator factories
    @classmethod
    def isExpression(self, string):
        """
        Check whether {string} is an expression
        """
        # NYI: this is not very smart; FIX IT
        return self.Expression._scanner.match(string)


    @classmethod
    def newExpression(self, formula, model, **kwds):
        """
        Build and return a new expression
        """
        return self.Expression(expression=formula, model=model, **kwds)
    

    @classmethod
    def newLiteral(self, value, **kwds):
        """
        Build and return a new expression
        """
        return self.Literal(value=value, **kwds)


    def newReference(self, **kwds):
        """
        Build and return a new reference to me
        """
        return self.__class__(value=None, evaluator=self.Reference(node=self), **kwds)


    # interface
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
        # if i am in the clean set, we are done
        if self in clean:
            return
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
        clean.add(self)
        # and return
        return self


    def flush(self):
        """
        Invalidate my cache and notify my observers
        """
        # invalidate my cache
        self._value = None
        # notify the observers
        self.notify()
        # and return
        return self


    def replace(self, *, node, name=None):
        """
        Remove {node} from its evaluation graph and graft {self} in its place
        """
        # flush the old node
        node.flush()
        # transfer the old observers
        self.addObservers(node)
        # and iterate through them to adjust their domain
        for observer in node._observers:
            # patch the observer's domain of the client
            observer._replace(name=name, old=node, new=self)
        # all done
        return self


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


    # implementation details
    def _getValue(self):
        """
        Refresh my value, if necessary, and return it
        """
        # if my cached value is invalid
        if self._value is None:
            # get my evaluator to refresh it
            try:
                self._value = self._evaluator and self._evaluator.compute()
            # leave unresolved node errors alone
            except self.UnresolvedNodeError:
                raise
            # dress anything else up as an EvaluationError
            except Exception as error:
                raise self.EvaluationError(evaluator=self, error=error) from error
        # and return it
        return self._value


    def _setValue(self, value):
        """
        Set my value to the passed literal value and notify my observers

        This implies that i do not need my evaluator any more, so it is destroyed
        """
        # refresh my cache
        self._value = value
        # clear out my evaluator
        self._evaluator  = self._prepareEvaluator(None)
        # invalidate my observers' caches
        self.notify()
        # and return
        return self


    def _setEvaluator(self, evaluator):
        """
        Install a new evaluator
        """
        # invalidate my cache
        self._value = None
        # install the new evaluator
        self._evaluator = self._prepareEvaluator(evaluator)
        # notify my observers
        self.notify()
        # and return
        return self


    def _prepareEvaluator(self, evaluator):
        """
        Handle the transition to a new evaluator gracefully
        """
        # if i already have an evaluator
        if self._evaluator is not None:
            # shut it down
            self._evaluator.finalize()
        # initialize the new evaluator
        if evaluator is not None:
            evaluator.initialize(owner=self)
        # and return it
        return evaluator


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
            for idx,op in enumerate(self._evaluator.getDomain()):
                print("       op {}: {}".format(idx, op))

        if self._observers:
            print("   observers:")
            for idx,observer in enumerate(self._observers):
                print("       {}: {}".format(idx, observer))
                print("           node: {}".format(observer.__self__))
                print("           func: {}".format(observer.__func__))

        return


    # private data
    _value = None
    _evaluator = None


# end of file 
