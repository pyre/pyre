# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# externals
import operator


# declaration
class Ordering:
    """
    This is a mix-in class that traps comparisons

    The point is to redirect comparisons among instances of subclasses of {Ordering} to methods
    defined in these subclasses. These methods then build and return representations of the
    corresponding operators and their operands.

    {Ordering} expects its subclasses to define {operator} to construct the operator
    representations. It is the responsibility of {operator} to handle foreign values correctly.

    N.B.: this mix-in overrides {__eq__} to return an operator node; this messes up naive
    equality tests, as well as the container membership tests that rely on it.
    """


    # overrides for the python standard methods
    # methods are listed in the order they show up in the python documentation
    def __eq__(self, other):
        # build a representation of the equality test
        return self.operator(evaluator=operator.eq, operands=(self, other))


    # and of course, now that we have overridden __eq__, we must specify this so that
    # {Ordering} instances can be keys of dictionaries and members of sets...
    __hash__ = object.__hash__


    def __ne__(self, other):
        # build a representation of the inequality test
        return self.operator(evaluator=operator.ne, operands=(self, other))


    def __le__(self, other):
        # build a representation of {<=}
        return self.operator(evaluator=operator.le, operands=(self, other))


    def __ge__(self, other):
        # build a representation of the equality test
        return self.operator(evaluator=operator.ge, operands=(self, other))


    def __lt__(self, other):
        # build a representation of the equality test
        return self.operator(evaluator=operator.lt, operands=(self, other))


    def __gt__(self, other):
        # build a representation of the equality test
        return self.operator(evaluator=operator.gt, operands=(self, other))


# end of file
