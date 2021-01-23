# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# externals
import operator


# declaration
class Boolean:
    """
    This is a mix-in class that traps the boolean operators

    The point is to redirect boolean operations among instances of subclasses of {Boolean} to
    methods defined in these subclasses. These methods then build and return representations of
    the corresponding operators and their operands.

    {Boolean} expects its subclasses to define {operator} to construct the operator
    representations. It is the responsibility of {operator} to handle foreign values correctly.
    """


    # logical operations
    def __and__(self, other):
        # build a representation of the operation
        return self.operator(evaluator=operator.and_, operands=(self, other))


    def __or__(self, other):
        # build a representation of the operation
        return self.operator(evaluator=operator.or_, operands=(self, other))


    # the reflections
    def __rand__(self, other):
        # build a representation of the operation
        return self.operator(evaluator=operator.and_, operands=(other, self))


    def __ror__(self, other):
        # build a representation of the operation
        return self.operator(evaluator=operator.or_, operands=(other, self))


# end of file
