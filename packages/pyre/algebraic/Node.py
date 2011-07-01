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


    # traversal of the nodes in my expression tree
    @property
    def pyre_dependencies(self):
        """
        Traverse my expression tree looking for leaf nodes
        """
        # just return myself
        yield self
        # and no more
        return


    # interface
    def pyre_eval(self, **kwds):
        """
        Compute the value of my expression tree
        """
        raise NotImplementedError(
            "class {.__class__.__name__!r} must implement 'pyre_eval'".format(self))


    def pyre_patch(self, *args, **kwds):
        """
        Sentinel method for node patching in expression trees
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
        # build a representation of subtraction out of {Addition} and {Opposite}
        from .Addition import Addition
        from .Opposite import Opposite
        # and return it
        return Addition(op1=self, op2=Opposite(op=other))

    
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
        # build a representation of division out of {Multiplication} and {Inverse}
        from .Inverse import Inverse
        from .Multiplication import Multiplication
        # and return it
        return Multiplication(op1=self, op2=Inverse(op=other))

    
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
        # build an addition representation
        from .Addition import Addition
        from .Opposite import Opposite
        # and return it
        return Addition(op1=other, op2=Opposite(op=self))

    
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
        # build a representation of division out of {Multiplication} and {Inverse}
        from .Inverse import Inverse
        from .Multiplication import Multiplication
        # and return it
        return Multiplication(op1=other, op2=Inverse(op=self))

    
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
    

# end of file 
