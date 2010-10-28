# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


class Field:
    """
    The base class for record descriptors. See {pyre.records.Record} for details.
    """

    # types
    from ..schema.Object import Object
    # support for field algebra
    from .Addition import Addition
    from .Subtraction import Subtraction
    from .Multiplication import Multiplication
    from .Division import Division
    from .FloorDivision import FloorDivision
    from .Remainder import Remainder
    from .Power import Power
    from .Plus import Plus
    from .Minus import Minus
    from .Absolute import Absolute


    # public data
    name = None # my name
    default = None # my default value
    optional = False # am i allowed to be uninitialized?
    type = Object # my type; most likely one of the pyre.schema type declarators
    validators = () # the chain of functions that inspect and validate my value
    converters = () # the chain of transformation necessary to produce a value in my native type


    # interface
    def eval(self, values, index):
        """
        Compute my value by looking up my offset in {index} and returning the corresponding
        slot from {values}
        """
        return values[index[self]]


    # algebra; methods are listed in the order they show up in the python docs
    def __add__(self, other):
        return self.Addition(op1=self, op2=other)
    
    def __sub__(self, other):
        return self.Subtraction(op1=self, op2=other)
    
    def __mul__(self, other):
        return self.Multiplication(op1=self, op2=other)
    
    def __truediv__(self, other):
        return self.Division(op1=self, op2=other)
    
    def __floordiv__(self, other):
        return self.FloorDivision(op1=self, op2=other)
    
    def __mod__(self, other):
        return self.Remainder(op1=self, op2=other)
    
    def __pow__(self, other):
        return self.Power(op1=self, op2=other)
    
    def __pos__(self):
        return self.Plus(op=self)
    
    def __neg__(self):
        return self.Minus(op=self)
    
    def __abs__(self):
        return self.Absolute(op=self)
    
    # reflected ones
    def __radd__(self, other):
        return self.Addition(op2=self, op1=other)
    
    def __rsub__(self, other):
        return self.Subtraction(op2=self, op1=other)
    
    def __rmul__(self, other):
        return self.Multiplication(op2=self, op1=other)
    
    def __rtruediv__(self, other):
        return self.Division(op2=self, op1=other)
    
    def __rfloordiv__(self, other):
        return self.FloorDivision(op2=self, op1=other)
    
    def __rmod__(self, other):
        return self.Remainder(op2=self, op1=other)
    
    def __rpow__(self, other):
        return self.Power(op2=self, op1=other)
    

# end of file 
