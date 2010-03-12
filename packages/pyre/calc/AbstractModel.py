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


    def addNode(self, name, node):
        """
        Implementation details of the mechanism for node insertion in the model.

        If you are looking to insert a node in the model, please use 'registerNode',
        which is a lot smarter and takes care of patching unresolved names.
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must implement 'addNode'".format(self))


    def findNode(self, name):
        """
        Locate the node in the model that matches {name}.
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must implement 'findNode'".format(self))
        

    def registerNode(self, *, name, node):
        """
        Add {node} into the model and make it accessible through {name}
        """
        # print("{0.name}: registering {1}".format(self, name))
        # attempt to find another node by the same name
        try:
            old = self.findNode(name)
            # print("  {0!r} is already in the model!".format(name))
        except KeyError:
            # add the node to the model
            self.addNode(name=name, node=node)
            # print("  added {0!r} to the model!".format(name))
            # check whether this is a registration for a node previously marked as unersolved
            try:
                # the old node is a previously unresolved one,
                # print("  looking for a matching unresolved node")
                unresolved = self._unresolvedNodes[name]
            except KeyError:
                # no, this is a new node; we are done
                return node

            # got one
            # print("  got it")
            # transfer the registered observers
            # print(
            # "  adjusting the observers of the new node: {0}"
            # .format(len(unresolved._observers)))
            node._observers |= unresolved._observers
            # patch its clients
            # print("  clients that need patching: {0}".format(unresolved.clients))
            for client in unresolved.clients:
                # replace the unresolved node in its domain with the new one
                # print("  fixing the domain of Evaluator@0x{0:x}".format(id(client)))
                client._replace(old=unresolved, new=node)
            # and remove it from the unresolved pile
            del self._unresolvedNodes[name]
            # and return the new node
            return node
        # otherwise it's a real collision
        raise self.DuplicateNodeError(model=self, name=name, node=old)


    def resolveNode(self, name, client):
        """
        Find the named node
        """
        # if {name} maps to an unresolved node
        try:
            # grab the node
            unresolved = self._unresolvedNodes[name]
            # add this client to its pile
            unresolved.clients.add(client)
            # and return it
            return unresolved
        except KeyError:
            pass
        # if {name} maps to a node already in the model
        try:
            # return it
            return self.findNode(name)
        except KeyError:
            pass
        # otherwise build an unresolved node rep
        from .UnresolvedNode import UnresolvedNode
        unresolved = UnresolvedNode(name=name, client=client)
        # add it to the pile
        self._unresolvedNodes[name] = unresolved
        # and return it
        return unresolved


    def getNodes(self):
        """
        Iterate over the nodes in my graph.

        This is expected to return a sequence of ({name}, {node}) tuples, regardless of the
        node storage details implemented by AbstractModel descendants
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must implement 'getNodes'".format(self))


    # exceptions
    from . import CircularReferenceError, DuplicateNodeError

    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        self._unresolvedNodes = {}
        return


    # subscripted access
    def __getitem__(self, name):
        return self.findNode(name).value

    def __setitem__(self, name, value):
        self.findNode(name).value = value
        return


    # debugging support
    def _dump(self):
        """
        List my contents
        """
        print("model {0!r}:".format(self.name))
        for name, node in self.getNodes():
            print("    {0!r}: {1!r}".format(name, node.value))
        return


    # implementation details
    # private data
    _cleanNodes = None # the set of nodes known to have no cycles
    _unresolvedNodes = None # the name map of unresolved nodes


# end of file 
