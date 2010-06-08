# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import pyre
from ..calc.Node import Node


class Variable(Node):
    """
    The object used to hold the values of all configurable items
    """


    # public data
    priority = (-1,-1)


    # interface
    def replace(self, other, alias):
        """
        Replace references to node {other} under the name {alias}, and steal its value if its
        priority is higher than mine
        """
        # print("      priorities: mine={0.priority!r}, hers={1.priority!r}".format(self, other))
        # if {other} has higher priority
        if self.priority < other.priority:
            # print("      overriding")
            # assume its value and priority
            self.value = other.value
            self.priority = other.priority
        # either way, she is redundant; so replace her
        return super().replace(node=other, name=alias)


    # meta methods
    def __init__(self, priority=priority, **kwds):
        super().__init__(**kwds)
        self.priority = priority
        return


    # implementation details
    def _setValue(self, value):
        # value==None implies the variable is uninitialized
        if value is None:
            return super()._setValue(value)
        # if the value is an instance of Evaluator, set the evaluator
        if isinstance(value, self.Evaluator):
            super()._setEvaluator(evaluator=value)
            calculator.validateNode(node=self)
            return self
        # if the value is a string that contains replacements markers, build an evaluator
        if isinstance(value, str) and self.Expression._scanner.match(value):
            calculator = pyre.executive().calculator
            evaluator=self.Expression(expression=value, model=calculator)
            super()._setEvaluator(evaluator)
            calculator.validateNode(node=self)
            return self
        # otherwise, just set the value
        return super()._setValue(value)


    # access to the expression evaluator
    from ..calc.Expression import Expression


# end of file 
