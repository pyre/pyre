# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from ..calc.AbstractModel import AbstractModel


class Evaluator(AbstractModel):
    """
    The keeper of all configurable values maintained by the framework

    It is implemented as pyre.calc.AbstractModel
    """


    # interface obligations from the abstract base class
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
        

    def getNodes(self):
        """
        Iterate over the nodes in my graph.

        This is expected to return a sequence of ({name}, {node}) tuples, regardless of the
        node storage details implemented by AbstractModel descendants
        """
        raise NotImplementedError(
            "class {0.__class__.__name__!r} must implement 'getNodes'".format(self))


    # meta methods
    def __init__(self, **kwds):
        super().__init__(name="pyre.evaluator", **kwds)
        return


# end of file 
