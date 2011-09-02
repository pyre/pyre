# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# access to the operator module
import operator


# declaration
class Number:
    """
    This is a mix-in class that traps the arithmetic operators relevant for numeric types

    The point is to redirect arithmetic among instances of subclasses of {Number} to methods
    defined in these subclasses. These methods then build and return representations of the
    corresponding operators and their operands.

    {Number} expects its subclasses to define two class methods: {literal} and {operation}. The
    former is used to encapsulate operands that are not {Number} instances. The latter is used
    to construct the operator representations
    """


    # overrides for the python standard methods
    # methods are listed in the order they show up in the python documentation
    def __add__(self, other):
        # if {other} is not a node
        if not isinstance(other, Number):
            # promote it
            other = self.literal(value=other)
        # build an addition representation
        return self.operation(operator=operator.add, operands=(self, other))

    
    def __sub__(self, other):
        # if {other} is not a node
        if not isinstance(other, Number):
            # promote it
            other = self.literal(value=other)
        # build a subtraction representation
        return self.operation(operator=operator.sub, operands=(self, other))

    
    def __mul__(self, other):
        # if {other} is not a node
        if not isinstance(other, Number):
            # promote it
            other = self.literal(value=other)
        # build a representation for multiplication
        return self.operation(operator=operator.mul, operands=(self, other))

    
    def __truediv__(self, other):
        # if {other} is not a node
        if not isinstance(other, Number):
            # promote it
            other = self.literal(value=other)
        # build a representation of division
        return self.operation(operator=operator.truediv, operands=(self, other))

    
    def __floordiv__(self, other):
        # if {other} is not a node
        if not isinstance(other, Number):
            # promote it
            other = self.literal(value=other)
        # build a representation of floor-division 
        return self.operation(operator=operator.floordiv, operands=(self, other))
    

    def __mod__(self, other):
        # if {other} is not a node
        if not isinstance(other, Number):
            # promote it
            other = self.literal(value=other)
        # build a modulus representation
        return self.operation(operator=operator.mod, operands=(self, other))
    

    def __pow__(self, other):
        # if {other} is not a node
        if not isinstance(other, Number):
            # promote it
            other = self.literal(value=other)
        # build a representation of exponentiation
        return self.operation(operator=operator.pow, operands=(self, other))
    

    def __pos__(self):
        return self

    
    def __neg__(self):
        return self.operation(operator=operator.neg, operands=(self,))

    
    def __abs__(self):
        return self.operation(operator=operator.abs, operands=(self,))

    
    # reflected ones: one operand was not a node, so it gets promoted through {literal}
    def __radd__(self, other):
        # {other} is not a node, so promote it
        other = self.literal(value=other)
        # build an addition representation
        return self.operation(operator=operator.add, operands=(other,self))

    
    def __rsub__(self, other):
        # {other} is not a node, so promote it
        other = self.literal(value=other)
        # build a subtraction representation
        return self.operation(operator=operator.sub, operands=(other,self))

    
    def __rmul__(self, other):
        # {other} is not a node, so promote it
        other = self.literal(value=other)
        # build a representation of multiplication
        return self.operation(operator=operator.mul, operands=(other,self))

    
    def __rtruediv__(self, other):
        # {other} is not a node, so promote it
        other = self.literal(value=other)
        # build a representation of division
        return self.operation(operator=operator.truediv, operands=(other,self))

    
    def __rfloordiv__(self, other):
        # {other} is not a node, so promote it
        other = self.literal(value=other)
        # build a representation of floor-division 
        return self.operation(operator=operator.floordiv, operands=(other,self))
    

    def __rmod__(self, other):
        # {other} is not a node, so promote it
        other = self.literal(value=other)
        # build a modulus representation
        return self.operation(operator=operator.mod, operands=(other,self))

    
    def __rpow__(self, other):
        # {other} is not a node, so promote it
        other = self.literal(value=other)
        # build a representation of exponentiation
        return self.operation(operator=operator.pow, operands=(other,self))


# end of file 
