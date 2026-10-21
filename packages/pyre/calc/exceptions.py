# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Definitions for all the exceptions raised by this package
"""

# pull the exceptions from {algebraic}
from ..algebraic.exceptions import NodeError, CircularReferenceError


# the local ones
class EvaluationError(NodeError):
    """
    Base class for node evaluation exceptions
    """

    # public data
    description = "evaluation error: {0.error}"

    # meta-methods
    def __init__(self, node=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the error info
        self.node = node
        # all done
        return


class ExpressionError(NodeError):
    """
    Base class for expression errors; useful when trapping them as a category
    """


class DisallowedNameError(ExpressionError):
    """
    Exception raised when the value of a setting uses a name that starts with two underscores,
    which reaches past the builtins it is allowed
    """

    # public data
    description = (
        "{0.name!r} can't be used in the value of a setting; "
        "names that start with two underscores are off limits"
    )

    # meta-methods
    def __init__(self, name, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the name
        self.name = name
        # all done
        return


class DisallowedFunctionError(DisallowedNameError):
    """
    Exception raised when the value of a setting uses a builtin it is not allowed
    """

    # public data
    description = (
        "{0.name!r} can't be used in the value of a setting; the functions allowed are\n"
        "{0.allowed}"
    )

    @property
    def allowed(self) -> str:
        """
        List the functions the value of a setting may use, a group per line
        """
        # get the groups
        from .evaluation import functions

        # render each group on a line of its own
        lines = (
            f"  {group}: {', '.join(function.__name__ for function in members)}"
            for group, members in functions.items()
        )
        # and put them together
        return "\n".join(lines)


class EmptyExpressionError(ExpressionError):
    """
    Exception raised when the expression factory did not encounter any named references to
    other nodes
    """

    # public data
    description = "while parsing {0.expression!r}: no references found"

    # meta-methods
    def __init__(self, formula, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the error info
        self.expression = formula
        # all done
        return


class ExpressionSyntaxError(ExpressionError):
    """
    Exception raised when the python interpreter encounters a syntax error while compiling the
    expression
    """

    # public data
    description = "while evaluating {0.expression!r}: {0.error}"

    # meta-methods
    def __init__(self, formula, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the error info
        self.expression = formula
        # all done
        return


class UnresolvedNodeError(NodeError):
    """
    Signal a value request from an unresolved node
    """

    # public data
    description = "node {0.name!r} is unresolved"

    # meta-methods
    def __init__(self, name, node=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the error info
        self.name = name
        self.node = node
        # all done
        return


class AliasingError(NodeError):
    """
    Signal that an alias was requested among names that were associated with existing nodes
    """

    # public data
    description = "both {0.target!r} and {0.alias!r} have existing nodes"

    # meta-methods
    def __init__(self, key, target, alias, targetNode, targetInfo, aliasNode, aliasInfo, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the error info
        self.key = key
        self.target = target
        self.alias = alias
        self.targetNode = targetNode
        self.targetInfo = targetInfo
        self.aliasNode = aliasNode
        self.aliasInfo = aliasInfo
        # all done
        return


# end of file
