# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


class Derivation:
    """
    The base class for descriptors whose value is derived from other fields in a record. See
    {pyre.records.Record} for more details
    """


    # public data
    name = None # my name


    # algebra; methods are listed in the order they show up in the python docs
    def __add__(self, other):
        from .Addition import Addition
        return Addition(op1=self, op2=other)
    
    def __sub__(self, other):
        from .Subtraction import Subtraction
        return Subtraction(op1=self, op2=other)
    
    def __mul__(self, other):
        from .Multiplication import Multiplication
        return Multiplication(op1=self, op2=other)
    
    def __truediv__(self, other):
        from .Division import Division
        return Division(op1=self, op2=other)
    
    def __floordiv__(self, other):
        from .FloorDivision import FloorDivision
        return FloorDivision(op1=self, op2=other)
    
    def __mod__(self, other):
        from .Remainder import Remainder
        return Remainder(op1=self, op2=other)
    
    def __pow__(self, other):
        from .Power import Power
        return Power(op1=self, op2=other)
    
    def __pos__(self):
        from .Plus import Plus
        return Plus(op=self)
    
    def __neg__(self):
        from .Minus import Minus
        return Minus(op=self)
    
    def __abs__(self):
        from .Absolute import Absolute
        return Absolute(op=self)
    
    # reflected ones
    def __radd__(self, other):
        from .Addition import Addition
        return Addition(op2=self, op1=other)
    
    def __rsub__(self, other):
        from .Subtraction import Subtraction
        return Subtraction(op2=self, op1=other)
    
    def __rmul__(self, other):
        from .Multiplication import Multiplication
        return Multiplication(op2=self, op1=other)
    
    def __rtruediv__(self, other):
        from .Division import Division
        return Division(op2=self, op1=other)
    
    def __rfloordiv__(self, other):
        from .FloorDivision import FloorDivision
        return FloorDivision(op2=self, op1=other)
    
    def __rmod__(self, other):
        from .Remainder import Remainder
        return Remainder(op2=self, op1=other)
    
    def __rpow__(self, other):
        from .Power import Power
        return Power(op2=self, op1=other)
    

# end of file 
