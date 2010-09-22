# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from ..patterns.Named import Named


class AbstractModel(Named):
    """
    An abstract evaluation context for nodes.

    AbstractModel provides the interface for managing nodes and delegates the actual storage
    mechanism to its descendants. 
    """


    # interface
    @property
    def nodes(self):
        """
        Create an iterable over the nodes in my graph.

        This is expected to return the complete sequence of nodes, regardless of the storage
        details implemented by AbstractModel descendants
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must implement 'nodes'".format(self))


    def register(self, *, name, node):
        """
        Add {node} into the model and make it accessible through {name}
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must implement 'register'".format(self))


    def resolve(self, name):
        """
        Find the named node
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must implement 'register'".format(self))


    def validate(self, root=None):
        """
        Attempt to validate the evaluation graph.
        
        Currently this performs the following steps:
            - detect cycles
            - ensure that all nodes in the network can compute their current values

        Any errors detected during validation currently raise exceptions and are not processed
        by this method. This may change.

        The network is valid only as long as no new nodes have been inserted since the last
        time it was validated
        """
        # if we are validating the subgraph anchored at a given node
        if root:
            # limit the scope
            scope = [root]
            # initialize the clean set
            self._cleanNodes.discard(root)
        # otherwise
        else:
            # visit all nodes in the model
            scope = self.nodes
            # initialize the clean set
            self._cleanNodes = set()

        # iterate over all the nodes looking for cycles
        for node in scope:
            node.validate(clean=self._cleanNodes)

        return


    # exceptions
    from .exceptions import (
        CircularReferenceError, DuplicateNodeError, ExpressionError, NodeError,
        UnresolvedNodeError
        )


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        self._cleanNodes = set()
        return


    # implementation details
    # private data
    _cleanNodes = None # the set of nodes known to have no cycles


# end of file 
