# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# access to the base class
from ..patterns.Named import Named


# declaration
class SymbolTable(Named):
    """
    The base class for node evaluation contexts

    {SymbolTable} provides the interface for managing nodes. The storage mechanism is delegated
    to subclasses.
    """


    # types
    # nodes
    from .Node import Node as node
    from .Variable import Variable as var
    from .Expression import Expression as expression
    from .UnresolvedNode import UnresolvedNode as unresolved
    # exceptions
    from .exceptions import (
        CircularReferenceError,
        EmptyExpressionError, ExpressionSyntaxError, EvaluationError,
        UnresolvedNodeError
        )


    # public data
    @property
    def nodes(self):
        """
        Create an iterable over the nodes in my graph.

        This is expected to return the complete sequence of nodes, regardless of the storage
        details implemented by AbstractModel descendants
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must implement 'nodes'".format(self))


    # interface
    def register(self, *, name, node):
        """
        Add {node} into the model and make it accessible through {name}
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must implement 'register'".format(self))


    def resolve(self, *, name):
        """
        Find the named node
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must implement 'resolve'".format(self))


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        self._cleanNodes = set()
        return


    # subscripted access to the model
    def __getitem__(self, name):
        """
        Resolve {name} into a node and return its value
        """
        # delegate
        return self.resolve(name=name).value


    def __setitem__(self, name, value):
        """
        Add/update the named node with the given {value}
        """
        # is {name} already known?
        existing = self.resolve(name)

        # if {value} is a string
        if isinstance(value, str):
            # attempt to convert it into an expression
            try:
                node = self.expression.parse(expression=value, model=self)
                # print("new node {!r}".format(name))
            # empty expressions are raw data; other errors propagate
            except self.EmptyExpressionError:
                node = self.var(value=value)
                # print("new node {!r}".format(name))
        # if {value} is already a node
        elif isinstance(value, self.node):
            # save it
            node = value
        # from here on, {value} is treated as raw data
        # if the existing node is a variable
        elif isinstance(existing, self.var):
            # adjust its value
            existing.value = value
            # and make it our working node
            node = existing
        # otherwise, {value} is raw data AND {existing} should be replaced
        else:
            # make a new one
            # print("new node {!r}".format(name))
            node = self.var(value=value)

        # checkpoint: if we've made a new node
        if node is not existing:
            # patch the model
            # print("patching {!r}: existing={}, new={}".format(name, existing, node))
            self.patch(discard=existing, keep=node)

        # register the new node
        self.register(name=name, node=node)
        # and return
        return self


    def patch(self, discard, keep):
        """
        Replace {discard} with {keep}

        N.B.: subclasses must implement this carefully as there are many model invariants that
        must be maintained...
        """
        # iterate over the observers of the discarded node
        for observer in tuple(discard.observers):
            # substitute the discarded node with its replacement
            observer.substitute(current=discard, replacement=keep)
        # and return
        return


    # private data
    _cleanNodes = None


# end of file 
