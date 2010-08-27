# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from ..calc.Node import Node


class Slot(Node):
    """
    Storage for trait values
    """


    # constants
    DEFAULT_PRIORITY = (-1,-1)



    # interface
    @classmethod
    def recognize(cls, value, configuration):
        """
        Convert {value} into a (value, evaluator) pair, as appropriate
        """
        # check whether {value} is the marker for uninitialized traits
        if value is None: return None
        # check whether {value} can be turned into an expression
        if isinstance(value, str) and cls.isExpression(value):
            # build an expression evaluator and return it
            return cls.newExpression(formula=value, model=configuration)
        # check whether {value} is an evaluator
        if isinstance(value, cls.Evaluator): return value
        # otherwise, build a literal evaluator and return it
        return cls.newLiteral(value=value)


    def assign(self, *, value=None, evaluator=None, priority=DEFAULT_PRIORITY):
        """
        Perform an assignment of the ({value}, {evaluator}) pair based on whether the requested
        {priority} overrides previous assignments
        """
        # check the priority of the request and bail out if it is not sufficiently high
        if self._priority > priority: return self

        # if i have an evaluator, shut it down
        if self._evaluator: self._evaluator.finalize()
        # if i were handed an evaluator, initialize it
        if evaluator: evaluator.initialize(owner=self)
 
        # make the assignments
        self._value = value
        self._evaluator = evaluator
        self._priority = priority

        # and return
        return self


    def replace(self, other, alias):
        """
        Replace references to node {other} under the name {alias}, and steal its value if its
        priority is higher than mine
        """
        # print("      priorities: mine={0._priority!r}, hers={1._priority!r}".format(self, other))
        # if {other} has higher priority
        if self._priority < other._priority:
            # print("      overriding")
            # shutdown my evaluator, if any
            if self._evaluator: self._evaluator.finalize()
            # assume its value and priority
            self._value = other._value
            self._evaluator = other._evaluator
            self._priority = other._priority
        # either way, she is redundant; so replace her
        return super().replace(node=other, name=alias)


    # meta methods
    def __init__(self, priority=DEFAULT_PRIORITY, **kwds):
        super().__init__(**kwds)
        self._priority = priority
        return


    # private data
    _priority = None


# end of file 
