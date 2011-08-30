# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# declaration
class Node:
    """
    This is the base class for hierarchies that implement the algebraic protocol

    The algebraic protocol is a strategy for deferring the evaluation of algebraic
    expressions. Participating classes can derive from {Node} to inherit the supplied
    implementations of the special methods that override the arithmetic operators. The actual
    evaluation is performed using the special method __call__ with whatever arguments your
    evaluation network requires. See the documentation of __call_ below for more details.
    """


    # traversal of the nodes in my expression graph
    @property
    def dependencies(self):
        """
        Traverse my expression graph looking for nodes i depend on
        """
        # just return myself
        yield self
        # and no more
        return


    # interface
    def eval(self, **kwds):
        """
        Compute the value of my expression graph
        """
        raise NotImplementedError(
            "class {.__class__.__name__!r} must implement 'eval'".format(self))


    def dfs(self, **kwds):
        """
        Traverse an expression graph in depth-first order
        """
        # by default, node instances yield themselves
        yield self
        # and no more
        return


    def patch(self, *args, **kwds):
        """
        Sentinel method for node patching in expression graphs
        """
        return


    # hooks for implementing the expression graph construction
    # the default implementation provided by this package uses the classes defined here
    def literal(self, value):
        """
        Build a representation of a foreign value
        """
        from .Literal import Literal
        return Literal(value)


    # arithmetic
    # operators are presented in the order the python methods appear in the python
    # documentation
    def addition(self, op1, op2):
        """
        Build a representation for addition
        """
        from .Addition import Addition
        return Addition(op1, op2)


    def subtraction(self, op1, op2):
        """
        Build a representation for subtraction
        """
        from .Subtraction import Subtraction
        return Subtraction(op1, op2)


    def multiplication(self, op1, op2):
        """
        Build a representation for multiplication
        """
        from .Multiplication import Multiplication
        return Multiplication(op1, op2)


    def division(self, op1, op2):
        """
        Build a representation for true division
        """
        from .Division import Division
        return Division(op1, op2)


    def floorDivision(self, op1, op2):
        """
        Build a representation for true division
        """
        from .FloorDivision import FloorDivision
        return FloorDivision(op1, op2)


    def modulus(self, op1, op2):
        """
        Build a representation for mod
        """
        from .Modulus import Modulus
        return Modulus(op1, op2)


    def power(self, op1, op2):
        """
        Build a representation for power
        """
        from .Power import Power
        return Power(op1, op2)


    def opposite(self, op):
        """
        Build a representation of unary minus
        """
        from .Opposite import Opposite
        return Opposite(op)


    def absolute(self, op):
        """
        Build a representation of the absolute value
        """
        from .Absolute import Absolute
        return Absolute(op)


    # logical operators
    def logicalAnd(self, op1, op2):
        """
        Build a representation of logical and
        """
        from .And import And
        return And(op1, op2)


    def logicalOr(self, op1, op2):
        """
        Build a representation of logical and
        """
        from .Or import Or
        return Or(op1, op2)


    # comparisons
    def equal(self, op1, op2):
        """
        Build a representation of equality testing
        """
        from .Equal import Equal
        return Equal(op1, op2)


    def notEqual(self, op1, op2):
        """
        Build a representation of inequality testing
        """
        from .NotEqual import NotEqual
        return NotEqual(op1, op2)


    def lessEqual(self, op1, op2):
        """
        Build a representation of {<=}
        """
        from .LessEqual import LessEqual
        return LessEqual(op1, op2)


    def greaterEqual(self, op1, op2):
        """
        Build a representation of {>=}
        """
        from .GreaterEqual import GreaterEqual
        return GreaterEqual(op1, op2)


    def less(self, op1, op2):
        """
        Build a representation of {<}
        """
        from .Less import Less
        return Less(op1, op2)


    def greater(self, op1, op2):
        """
        Build a representation of {>}
        """
        from .Greater import Greater
        return Greater(op1, op2)


    # overrides for the python standard methods
    # methods are listed in the order they show up in the python documentation
    def __add__(self, other):
        # if {other} is not a node
        if not isinstance(other, Node):
            # promote it
            other = self.literal(value=other)
        # build an addition representation
        return self.addition(op1=self, op2=other)

    
    def __sub__(self, other):
        # if {other} is not a node
        if not isinstance(other, Node):
            # promote it
            other = self.literal(value=other)
        # build a subtraction representation
        return self.subtraction(op1=self, op2=other)

    
    def __mul__(self, other):
        # if {other} is not a node
        if not isinstance(other, Node):
            # promote it
            other = self.literal(value=other)
        # build a representation for multiplication
        return self.multiplication(op1=self, op2=other)

    
    def __truediv__(self, other):
        # if {other} is not a node
        if not isinstance(other, Node):
            # promote it
            other = self.literal(value=other)
        # build a representation of division
        return self.division(op1=self, op2=other)

    
    def __floordiv__(self, other):
        # if {other} is not a node
        if not isinstance(other, Node):
            # promote it
            other = self.literal(value=other)
        # build a representation of floor-division 
        return self.floorDivision(op1=self, op2=other)
    

    def __mod__(self, other):
        # if {other} is not a node
        if not isinstance(other, Node):
            # promote it
            other = self.literal(value=other)
        # build a modulus representation
        return self.modulus(op1=self, op2=other)
    

    def __pow__(self, other):
        # if {other} is not a node
        if not isinstance(other, Node):
            # promote it
            other = self.literal(value=other)
        # build a representation of exponentiation
        return self.power(op1=self, op2=other)
    

    def __pos__(self):
        return self

    
    def __neg__(self):
        return self.opposite(op=self)

    
    def __abs__(self):
        return self.absolute(op=self)

    
    # reflected ones: one operand was not a node, so it gets promoted through {Literal}
    def __radd__(self, other):
        # {other} is not a node, so promote it
        other = self.literal(value=other)
        # build an addition representation
        return self.addition(op1=other, op2=self)

    
    def __rsub__(self, other):
        # {other} is not a node, so promote it
        other = self.literal(value=other)
        # build a subtraction representation
        return self.subtraction(op1=other, op2=self)

    
    def __rmul__(self, other):
        # {other} is not a node, so promote it
        other = self.literal(value=other)
        # build a representation of multiplication
        return self.multiplication(op1=other, op2=self)

    
    def __rtruediv__(self, other):
        # {other} is not a node, so promote it
        other = self.literal(value=other)
        # build a representation of division
        return self.division(op1=other, op2=self)

    
    def __rfloordiv__(self, other):
        # {other} is not a node, so promote it
        other = self.literal(value=other)
        # build a representation of floor-division 
        return self.floorDivision(op1=other, op2=self)
    

    def __rmod__(self, other):
        # {other} is not a node, so promote it
        other = self.literal(value=other)
        # build a modulus representation
        return self.modulus(op1=other, op2=self)

    
    def __rpow__(self, other):
        # {other} is not a node, so promote it
        other = self.literal(value=other)
        # build a representation of exponentiation
        return self.power(op1=other, op2=self)


    # logical operations
    def __and__(self, other):
        # if {other} is not a node
        if not isinstance(other, Node):
            # promote it
            other = self.literal(value=other)
        # build a representation of the equality test
        return self.logicalAnd(op1=self, op2=other)


    def __or__(self, other):
        # if {other} is not a node
        if not isinstance(other, Node):
            # promote it
            other = self.literal(value=other)
        # build a representation of the equality test
        return self.logicalOr(op1=self, op2=other)


    # comparisons
    def __eq__(self, other):
        # if {other} is not a node
        if not isinstance(other, Node):
            # promote it
            other = self.literal(value=other)
        # build a representation of the equality test
        return self.equal(op1=self, op2=other)

    # and of course, now that we have overridden __eq__, we must specify this so that {Node}s
    # can be keys of dictionaries and members of sets...
    __hash__ = object.__hash__


    def __ne__(self, other):
        # if {other} is not a node
        if not isinstance(other, Node):
            # promote it
            other = self.literal(value=other)
        # build a representation of the equality test
        return self.notEqual(op1=self, op2=other)


    def __le__(self, other):
        # if {other} is not a node
        if not isinstance(other, Node):
            # promote it
            other = self.literal(value=other)
        # build a representation of {<=}
        return self.lessEqual(op1=self, op2=other)
        

    def __ge__(self, other):
        # if {other} is not a node
        if not isinstance(other, Node):
            # promote it
            other = self.literal(value=other)
        # build a representation of the equality test
        return self.greaterEqual(op1=self, op2=other)
        

    def __lt__(self, other):
        # if {other} is not a node
        if not isinstance(other, Node):
            # promote it
            other = self.literal(value=other)
        # build a representation of the equality test
        return self.less(op1=self, op2=other)
        

    def __gt__(self, other):
        # if {other} is not a node
        if not isinstance(other, Node):
            # promote it
            other = self.literal(value=other)
        # build a representation of the equality test
        return self.greater(op1=self, op2=other)
        

# end of file 
