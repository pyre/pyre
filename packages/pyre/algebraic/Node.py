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
    def pyre_dependencies(self):
        """
        Traverse my expression graph looking for leaf nodes
        """
        # just return myself
        yield self
        # and no more
        return


    # interface
    def pyre_eval(self, **kwds):
        """
        Compute the value of my expression graph
        """
        raise NotImplementedError(
            "class {.__class__.__name__!r} must implement 'pyre_eval'".format(self))


    def pyre_dfs(self, **kwds):
        """
        Traverse an expression graph in depth-first order
        """
        # by default, node instances yield themselves
        yield self
        # and no more
        return


    def pyre_patch(self, *args, **kwds):
        """
        Sentinel method for node patching in expression graphs
        """
        return


    # algebra; methods are listed in the order they show up in the python documentation
    def __add__(self, other):
        # if {other} is not a node
        if not isinstance(other, Node):
            # promote it
            from .Literal import Literal
            other = Literal(value=other)
        # build an addition representation
        from .Addition import Addition
        # and return it
        return Addition(op1=self, op2=other)

    
    def __sub__(self, other):
        # if {other} is not a node
        if not isinstance(other, Node):
            # promote it
            from .Literal import Literal
            other = Literal(value=other)
        # build a subtraction representation
        from .Subtraction import Subtraction
        # and return it
        return Subtraction(op1=self, op2=other)

    
    def __mul__(self, other):
        # if {other} is not a node
        if not isinstance(other, Node):
            # promote it
            from .Literal import Literal
            other = Literal(value=other)
        # build a representation for multiplication
        from .Multiplication import Multiplication
        # and return it
        return Multiplication(op1=self, op2=other)

    
    def __truediv__(self, other):
        # if {other} is not a node
        if not isinstance(other, Node):
            # promote it
            from .Literal import Literal
            other = Literal(value=other)
        # build a representation of division
        from .Division import Division
        # and return it
        return Division(op1=self, op2=other)

    
    def __floordiv__(self, other):
        # if {other} is not a node
        if not isinstance(other, Node):
            # promote it
            from .Literal import Literal
            other = Literal(value=other)
        # build a representation of floor-division 
        from .FloorDivision import FloorDivision
        # and return it
        return FloorDivision(op1=self, op2=other)
    

    def __mod__(self, other):
        # if {other} is not a node
        if not isinstance(other, Node):
            # promote it
            from .Literal import Literal
            other = Literal(value=other)
        # build a modulus representation
        from .Modulus import Modulus
        # and return it
        return Modulus(op1=self, op2=other)
    

    def __pow__(self, other):
        # if {other} is not a node
        if not isinstance(other, Node):
            # promote it
            from .Literal import Literal
            other = Literal(value=other)
        # build a representation of exponentiation
        from .Power import Power
        # and return it
        return Power(op1=self, op2=other)
    

    def __pos__(self):
        return self

    
    def __neg__(self):
        from .Opposite import Opposite
        return Opposite(op=self)

    
    def __abs__(self):
        from .Absolute import Absolute
        return Absolute(op=self)

    
    # reflected ones: one operand was not a node, so it gets promoted through {Literal}
    def __radd__(self, other):
        # {other} is not a node, so promote it
        from .Literal import Literal
        other = Literal(value=other)
        # build an addition representation
        from .Addition import Addition
        # and return it
        return Addition(op1=other, op2=self)

    
    def __rsub__(self, other):
        # {other} is not a node, so promote it
        from .Literal import Literal
        other = Literal(value=other)
        # build a subtraction representation
        from .Subtraction import Subtraction
        # and return it
        return Subtraction(op1=other, op2=self)

    
    def __rmul__(self, other):
        # {other} is not a node, so promote it
        from .Literal import Literal
        other = Literal(value=other)
        # build a representation of multiplication
        from .Multiplication import Multiplication
        # and return it
        return Multiplication(op1=other, op2=self)

    
    def __rtruediv__(self, other):
        # {other} is not a node, so promote it
        from .Literal import Literal
        other = Literal(value=other)
        # build a representation of division
        from .Division import Division
        # and return it
        return Division(op1=other, op2=self)

    
    def __rfloordiv__(self, other):
        # {other} is not a node, so promote it
        from .Literal import Literal
        other = Literal(value=other)
        # build a representation of floor-division 
        from .FloorDivision import FloorDivision
        # and return it
        return FloorDivision(op1=other, op2=self)
    

    def __rmod__(self, other):
        # {other} is not a node, so promote it
        from .Literal import Literal
        other = Literal(value=other)
        # build a modulus representation
        from .Modulus import Modulus
        # and return it
        return Modulus(op1=other, op2=self)

    
    def __rpow__(self, other):
        # {other} is not a node, so promote it
        from .Literal import Literal
        other = Literal(value=other)
        # build a representation of exponentiation
        from .Power import Power
        # and return it
        return Power(op1=other, op2=self)


    # logical operations
    def __and__(self, other):
        # if {other} is not a node
        if not isinstance(other, Node):
            # promote it
            from .Literal import Literal
            other = Literal(value=other)
        # build a representation of the equality test
        from .And import And
        # and return it
        return And(op1=self, op2=other)


    def __or__(self, other):
        # if {other} is not a node
        if not isinstance(other, Node):
            # promote it
            from .Literal import Literal
            other = Literal(value=other)
        # build a representation of the equality test
        from .Or import Or
        # and return it
        return Or(op1=self, op2=other)


    # comparisons
    def __eq__(self, other):
        # if {other} is not a node
        if not isinstance(other, Node):
            # promote it
            from .Literal import Literal
            other = Literal(value=other)
        # build a representation of the equality test
        from .Equal import Equal
        # and return it
        return Equal(op1=self, op2=other)

    # and of course, now that we have overridden __eq__, we must specify this so that {Node}s
    # can be keys of dictionaries and members of sets...
    __hash__ = object.__hash__


    def __ne__(self, other):
        # if {other} is not a node
        if not isinstance(other, Node):
            # promote it
            from .Literal import Literal
            other = Literal(value=other)
        # build a representation of the equality test
        from .NotEqual import NotEqual
        # and return it
        return NotEqual(op1=self, op2=other)


    def __le__(self, other):
        # if {other} is not a node
        if not isinstance(other, Node):
            # promote it
            from .Literal import Literal
            other = Literal(value=other)
        # build a representation of the equality test
        from .LessEqual import LessEqual
        # and return it
        return LessEqual(op1=self, op2=other)
        

    def __ge__(self, other):
        # if {other} is not a node
        if not isinstance(other, Node):
            # promote it
            from .Literal import Literal
            other = Literal(value=other)
        # build a representation of the equality test
        from .GreaterEqual import GreaterEqual
        # and return it
        return GreaterEqual(op1=self, op2=other)
        

    def __lt__(self, other):
        # if {other} is not a node
        if not isinstance(other, Node):
            # promote it
            from .Literal import Literal
            other = Literal(value=other)
        # build a representation of the equality test
        from .Less import Less
        # and return it
        return Less(op1=self, op2=other)
        

    def __gt__(self, other):
        # if {other} is not a node
        if not isinstance(other, Node):
            # promote it
            from .Literal import Literal
            other = Literal(value=other)
        # build a representation of the equality test
        from .Greater import Greater
        # and return it
        return Greater(op1=self, op2=other)
        

# end of file 
