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
    def validate(self):
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
        # initialize the clean node set
        good = set()
        # iterate over all the nodes looking for cycles
        for name, node in self.getNodes():
            node.validate(span=set(), clean=good)
        # iterate over all the nodes ensuring that all nodes can compute their value
        for name, node in self.getNodes():
            node.value

        return


    def registerNode(self, *, name, node):
        """
        Add {node} into the model and make it accessible through {name}
        """
        # check whether this name has already been registered
        try:
            unresolved = self.findNode(name)
        except KeyError:
            # nope, this is the first time
            return self.addNode(name=name, node=node)
        # so, we have seen this name before
        # if it does not belong to an unresolved node
        if name not in self._unresolvedNames:
            # this is a name collision
            raise self.DuplicateNodeError(model=self, name=name, node=unresolved)
        # patching time...
        node.replace(node=unresolved, name=name)
        # remove the name from the unresolved pile
        self._unresolvedNames.remove(name)
        # and place the node in the model
        return self.addNode(name=name, node=node)


    def resolveNode(self, name, client):
        """
        Find the named node
        """
        # attempt to return the node that is registered under {name}
        try:
            return self.findNode(name)
        except KeyError:
            pass
        # otherwise, build an unresolved node
        from .UnresolvedNode import UnresolvedNode
        unresolved = self.newErrorNode(evaluator=UnresolvedNode(name))
        # add it to the pile
        self.addNode(name=name, node=unresolved)
        # and store the name so we can track these guys down
        self._unresolvedNames.add(name)
        # and return it
        return unresolved


    # methods that subclasses should override
    def newErrorNode(self, evaluator):
        """
        Create a new error node with the given evaluator
        """
        # why is this the right node factory?
        # subclasses should override this to provide their own nodes to host the error evaluator
        from .Node import Node
        return Node(value=None, evaluator=evaluator)


    # abstract methods that must be overriden by descendants
    def addNode(self, name, node):
        """
        Implementation details of the mechanism for node insertion in the model.

        If you are looking to insert a node in the model, please use 'registerNode',
        which is a lot smarter and takes care of patching unresolved names.

        Do not be tempted to detect duplicate names here; registerNode takes care of that. Just
        add the node to whatever storage mechanism you use and return the same node to the
        caller
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must implement 'addNode'".format(self))


    def findNode(self, name):
        """
        Locate the node in the model that matches {name}.
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must implement 'findNode'".format(self))
        

    def getNodes(self):
        """
        Iterate over the nodes in my graph.

        This is expected to return a sequence of ({name}, {node}) tuples, regardless of the
        node storage details implemented by AbstractModel descendants
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must implement 'getNodes'".format(self))


    # exceptions
    from .exceptions import (
        CircularReferenceError, DuplicateNodeError, ExpressionError, NodeError,
        UnresolvedNodeError
        )


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        self._unresolvedNames = set()
        return


    # subscripted access
    def __getitem__(self, name):
        return self.findNode(name).value

    def __setitem__(self, name, value):
        self.findNode(name).value = value
        return


    # debugging support
    def _dump(self, pattern=None):
        """
        List my contents
        """
        # build the node name recognizer
        import re
        regex = re.compile(pattern if pattern else '')

        print("model {0!r}:".format(self.name))
        for name, node in self.getNodes():
            if regex.match(name):
                print("    {0!r}: {1!r}".format(name, node.value))
        return


    # implementation details
    # private data
    _cleanNodes = None # the set of nodes known to have no cycles
    _unresolvedNames = None # the name map of unresolved nodes


# end of file 
