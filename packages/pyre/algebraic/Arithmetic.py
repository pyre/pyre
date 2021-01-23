# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# access to the operator module
import operator


# declaration
class Arithmetic:
    """
    This is a mix-in class that traps the arithmetic operators relevant for numeric types

    The point is to redirect arithmetic among instances of subclasses of {Arithmetic} to
    methods defined in these subclasses. These methods then build and return representations of
    the corresponding operators and their operands.

    {Arithmetic} expects its subclasses to define {operator} to construct the operator
    representations. It is the responsibility of {operator} to handle foreign values correctly.
    """


    # overrides for the python standard methods
    # methods are listed in the order they show up in the python documentation
    def __add__(self, other):
        # build an addition representation
        return self.operator(evaluator=operator.add, operands=(self, other))


    def __sub__(self, other):
        # build a subtraction representation
        return self.operator(evaluator=operator.sub, operands=(self, other))


    def __mul__(self, other):
        # build a representation for multiplication
        return self.operator(evaluator=operator.mul, operands=(self, other))


    def __truediv__(self, other):
        # build a representation of division
        return self.operator(evaluator=operator.truediv, operands=(self, other))


    def __floordiv__(self, other):
        # build a representation of floor-division
        return self.operator(evaluator=operator.floordiv, operands=(self, other))


    def __mod__(self, other):
        # build a modulus representation
        return self.operator(evaluator=operator.mod, operands=(self, other))


    def __pow__(self, other):
        # build a representation of exponentiation
        return self.operator(evaluator=operator.pow, operands=(self, other))


    def __pos__(self):
        return self


    def __neg__(self):
        return self.operator(evaluator=operator.neg, operands=(self,))


    def __abs__(self):
        return self.operator(evaluator=operator.abs, operands=(self,))


    # reflected ones: one operand was not a node, so it gets promoted through {literal}
    def __radd__(self, other):
        # build an addition representation
        return self.operator(evaluator=operator.add, operands=(other, self))


    def __rsub__(self, other):
        # build a subtraction representation
        return self.operator(evaluator=operator.sub, operands=(other, self))


    def __rmul__(self, other):
        # build a representation of multiplication
        return self.operator(evaluator=operator.mul, operands=(other, self))


    def __rtruediv__(self, other):
        # build a representation of division
        return self.operator(evaluator=operator.truediv, operands=(other, self))


    def __rfloordiv__(self, other):
        # build a representation of floor-division
        return self.operator(evaluator=operator.floordiv, operands=(other, self))


    def __rmod__(self, other):
        # build a representation for modulus
        return self.operator(evaluator=operator.mod, operands=(other, self))


    def __rpow__(self, other):
        # build a representation of exponentiation
        return self.operator(evaluator=operator.pow, operands=(other, self))


# end of file
