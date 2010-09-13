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
        # check whether {value} is already an evaluator
        if isinstance(value, cls.Evaluator): return value
        # build a literal for non-strings
        if not isinstance(value, str): return cls.newLiteral(value=value)
        # check whether {value} can be turned into an expression
        try:
            return cls.newExpression(formula=value, model=configuration)
        # convert empty expressions into literals
        except cls.EmptyExpressionError:
            # build a literal evaluator and return it
            return cls.newLiteral(value=value)
        # convert poorly formed expressions into literals
        except cls.ExpressionError:
            # build a literal evaluator and return it
            return cls.newLiteral(value=value)


    def assign(self, *, value=None, evaluator=None, priority=DEFAULT_PRIORITY):
        """
        Perform an assignment of the ({value}, {evaluator}) pair based on whether the requested
        {priority} overrides previous assignments
        """
        # check the priority of the request and bail out if it is not sufficiently high
        if self._priority > priority: return self

        # if i have an evaluator, shut it down
        if self._evaluator: self._evaluator.finalize(owner=self)
        # if i were handed an evaluator, initialize it
        if evaluator: evaluator.initialize(owner=self)
 
        # make the assignments
        self._value = value
        self._evaluator = evaluator
        self._priority = priority

        # and return
        return self


    def cede(self, replacement):
        """
        Remove {self} from my evaluation graph and graft {replacement} in my place. If my
        priority is higher, graft my value, evaluator and priority in my {replacement}
        """
        # print("      priorities: mine={0._priority!r}, hers={1._priority!r}".format(self, other))
        # if {other} has higher priority
        if replacement._priority < self._priority:
            # print("      overriding")
            # shutdown my evaluator, if any
            if replacement._evaluator: self._evaluator.finalize(owner=self)
            # assume its value and priority
            replacement._value = self._value
            replacement._evaluator = self._evaluator
            replacement._priority = self._priority
        # either way, I am redundant; so replace me
        return super().cede(replacement=replacement)


    # meta methods
    def __init__(self, priority=DEFAULT_PRIORITY, **kwds):
        super().__init__(**kwds)
        self._priority = priority
        return


    # exceptions
    from pyre.calc.exceptions import EmptyExpressionError, ExpressionError


    # private data
    _priority = None


# end of file 
