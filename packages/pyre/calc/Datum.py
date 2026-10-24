# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from ..algebraic.AbstractNode import AbstractNode


# declaration of the base node
class Datum(AbstractNode):
    """
    The base class for nodes that have values
    """

    # types
    # augmented structural nodes
    from .Composite import Composite as composite

    # new leaves
    mapping = None  # nodes that hold maps of nodes
    sequence = None  # nodes that hold sequences of nodes
    expression = None  # nodes that evaluate expressions
    interpolation = None  # nodes that interpolate text
    reference = None  # nodes that refer to other nodes
    unresolved = None  # markers of names nobody has set

    # exceptions; included here for client convenience
    from .exceptions import (
        NodeError,
        EmptyExpressionError,
        ExpressionSyntaxError,
        EvaluationError,
        UnresolvedNodeError,
    )

    # public data
    keep = False  # whether i follow the nodes i refer to only until my value is first read

    @property
    def value(self):
        """
        Get my value
        """
        # attempt to
        try:
            # ask me for my value
            value = self.getValue()
        # if reading is not supported
        except AttributeError:
            # complain
            raise self.EvaluationError(node=self, error="node value is not readable")
        # if all goes well, return the {value}
        return value

    @value.setter
    def value(self, value):
        """
        Set my value
        """
        # attempt to
        try:
            # set my value
            self.setValue(value=value)
        # if writing is not supported
        except AttributeError:
            # complain
            raise self.EvaluationError(node=self, error="node value is not writable")
        # all done
        return

    # classifiers
    @property
    def expressions(self):
        """
        Return a sequence over the nodes in my dependency graph that are constructed out of python
        expressions involving the names of other nodes
        """
        # by default, empty
        return ()

    @property
    def interpolations(self):
        """
        Return a sequence over the nodes in my dependency graph that are constructed by expanding
        the values of other nodes in a macro
        """
        # by default, empty
        return ()

    @property
    def mappings(self):
        """
        Return a sequence over the nodes in my dependency graph that are mappings
        """
        # by default, empty
        return ()

    @property
    def references(self):
        """
        Return a sequence over the nodes in my dependency graph that are references to other nodes
        """
        # by default, empty
        return ()

    @property
    def sequences(self):
        """
        Return a sequence over the nodes in my dependency graph that are sequences
        """
        # by default, empty
        return ()

    @property
    def unresolveds(self):
        """
        Return a sequence over the nodes in my dependency graph that represent requests for model
        names that don't exist
        """
        # by default, empty
        return ()

    # interface
    def ref(self, **kwds):
        """
        Build and return a reference to me
        """
        # use the class factory to make one and return it
        return self.reference(operands=(self,), **kwds)

    # debugging support
    def dump(self, name, indent):
        """
        Print my name and value
        """
        # attempt to
        try:
            # get my value
            value = self.value
        # if something goes wrong
        except self.NodeError as error:
            # use the error message as a value so the caller can see what's wrong
            value = f" ** ERROR: {error}"

        # show me
        print(f"{indent}{name}: {value}")

        # all done
        return self


# end of file
