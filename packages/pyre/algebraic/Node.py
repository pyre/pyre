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
    def dependencies(self):
        """
        Traverse my expression tree looking for leaf nodes
        """
        # just return myself
        yield self


    # algebra; methods are listed in the order they show up in the python documentation
    def __add__(self, other):
        # if this an operation among nodes
        if isinstance(other, Node):
            # build an addition representation
            from .Addition import Addition
            # and return it
            return Addition(op1=self, op2=other)
        # otherwise, build an increment node
        from .Increment import Increment
        # and return it
        return Increment(op=self, value=other)

    
    def __sub__(self, other):
        # if this an operation among nodes
        if isinstance(other, Node):
            # build a subtraction representation out of Addition and Opposite
            from .Addition import Addition
            from .Opposite import Opposite
            # and return it
            return Addition(op1=self, op2=Opposite(op=other))
        # otherwise, increment my opposite by other
        from .Increment import Increment
        # and return it
        return Increment(op=self, value=-other)

    
    def __mul__(self, other):
        # if this an operation among nodes
        if isinstance(other, Node):
            # build an addition representation
            from .Multiplication import Multiplication
            # and return it
            return Multiplication(op1=self, op2=other)
        # otherwise, build a scaling node
        from .Scaling import Scaling
        # and return it
        return Scaling(op=self, value=other)

    
    def __truediv__(self, other):
        # if this an operation among nodes
        if isinstance(other, Node):
            # build a representation of division out of Multiplication and Inverse
            from .Inverse import Inverse
            from .Multiplication import Multiplication
            # and return it
            return Multiplication(op1=self, op2=Inverse(op=other))
        # otherwise, build a scaling node
        from .Scaling import Scaling
        # and return it
        return Scaling(op=self, value=1/other)

    
    def __floordiv__(self, other):
        # if this an operation among nodes
        if isinstance(other, Node):
            # build an addition representation
            from .FloorDivision import FloorDivision
            # and return it
            return FloorDivision(op1=self, op2=other)
        # otherwise, build an increment node
        from .LeftFloorDivision import LeftFloorDivision
        # and return it
        return LeftFloorDivision(op=self, value=other)
    

    def __mod__(self, other):
        # if this an operation among nodes
        if isinstance(other, Node):
            # build an addition representation
            from .Modulus import Modulus
            # and return it
            return Modulus(op1=self, op2=other)
        # otherwise, build an increment node
        from .LeftModulus import LeftModulus
        # and return it
        return LeftModulus(op=self, value=other)
    

    def __pow__(self, other):
        # if this an operation among nodes
        if isinstance(other, Node):
            # build an addition representation
            from .Power import Power
            # and return it
            return Power(op1=self, op2=other)
        # otherwise, build an increment node
        from .LeftPower import LeftPower
        # and return it
        return LeftPower(op=self, value=other)
    

    def __pos__(self):
        return self

    
    def __neg__(self):
        from .Opposite import Opposite
        return Opposite(op=self)

    
    def __abs__(self):
        from .Absolute import Absolute
        return Absolute(op=self)

    
    # reflected ones
    def __radd__(self, other):
        # convert the operation to an increment node
        from .Increment import Increment
        # and return it
        return Increment(op=self, value=other)

    
    def __rsub__(self, other):
        # convert the operation to an increment node
        from .Opposite import Opposite
        from .Increment import Increment
        # and return it
        return Increment(op=Opposite(op=self), value=other)

    
    def __rmul__(self, other):
        # convert the operation to a scaling
        from .Scaling import Scaling
        # and return it
        return Scaling(op=self, value=other)

    
    def __rtruediv__(self, other):
        # convert the operation to a scaling
        from .Inverse import Inverse
        from .Scaling import Scaling
        # and return it
        return Scaling(op=Inverse(op=self), value=other)

    
    def __rfloordiv__(self, other):
        # convert the operation to a right floor division
        from .RightFloorDivision import RightFloorDivision
        # and return it
        return RightFloorDivision(op=self, value=other)
    

    def __rmod__(self, other):
        # convert the operation to a right remainder
        from .RightModulus import RightModulus
        # and return it
        return RightModulus(op=self, value=other)

    
    def __rpow__(self, other):
        # convert the operation to a right power
        from .RightPower import RightPower
        # and return it
        return RightPower(op=self, value=other)
    

# end of file 
