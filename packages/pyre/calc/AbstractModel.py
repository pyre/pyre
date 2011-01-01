# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from ..patterns.Named import Named


class AbstractModel(Named):
    """
    An abstract evaluation context for nodes.

    AbstractModel provides the interface for managing nodes and delegates the actual storage
    mechanism to its descendants. 
    """


    # types
    from .Node import Node as nodeFactory
    from .Node import Node
    from .Evaluator import Evaluator
    from .Expression import Expression
    from .Literal import Literal
    from .Reference import Reference


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


    def resolve(self, *, name):
        """
        Find the named node
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must implement 'register'".format(self))


    def patch(self, *, discard, keep):
        """
        Patch the evaluation graph by grafting {new} in the place of {old}
        """
        # transfer information from the throw away to the keeper
        keep.merge(other=discard)
        # all done
        return keep


    def recognize(self, value, **kwds):
        """
        Attempt to decipher {value} and convert it into a proper node
        """
        # identify what kind of value we were given
        # if {value} is another node
        if isinstance(value, self.Node): 
            # easy enough
            return value.newReference()
        # if {value} is an evaluator 
        if isinstance(value, self.Evaluator):
            # build a node with this evaluator
            return value
        # if it is a string
        if isinstance(value, str):
            # check whether it is an expression
            try:
                return self.Expression.parse(expression=value, model=self)
            except self.NodeError:
                # treat it like a literal
                return self.Literal(value=value)
        # otherwise
        # build a literal
        return self.Literal(value=value)


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


    # subscripted access
    def __getitem__(self, name):
        #  this is easy: get resolve to hunt down the node associated with {name}
        return self.resolve(name=name).value


    def __setitem__(self, name, value):
        # if {value} is alreay a node
        if isinstance(value, self.nodeFactory):
            node = value
        # otherwise, get the node factory to build one
        else:
            node = self.nodeFactory(value=None, evaluator=self.recognize(value))
        # now, let register do its magic
        self.register(name=name, node=node)
        # all done
        return


    # implementation details
    # private data
    _cleanNodes = None # the set of nodes known to have no cycles


# end of file 
