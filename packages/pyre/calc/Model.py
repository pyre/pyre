# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .AbstractModel import AbstractModel


class Model(AbstractModel):
    """
    Storage and naming services for calc nodes
    """


    # interface
    def addNode(self, name, node):
        """
        Implementation details of the mechanism for node insertion in the model.

        If you are looking to insert a node in the model, please use 'registerNode',
        which is a lot smarter and takes care of patching unresolved names.

        Do not be tempted to detect duplicate names here; registerNode takes care of that. Just
        add the node to whatever storage mechanism you use and return the same node to the
        caller
        """
        self._nodes[name] = node
        return node


    def findNode(self, name):
        """
        Locate the node in the model that matches {name}
        """
        return self._nodes[name]


    def getNodes(self):
        """
        Iterate over the nodes in my graph. Returns a sequence of ({name}, {node}) tuples.
        """
        return self._nodes.items()


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)
        self._nodes = {}
        return


# end of file 
