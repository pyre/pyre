# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import pyre.patterns
import pyre.tracking
from ..calc.AbstractModel import AbstractModel

from .Variable import Variable
from ..calc.Expression import Expression


class Calculator(AbstractModel):
    """
    The keeper of all configurable values maintained by the framework

    It is implemented as pyre.calc.AbstractModel
    """


    # constants
    SEPARATOR = '.'


    # interface
    def bind(self, name, value, locator, replace):
        """
        Bind the variable {name} to {value}.

        If there is no existing variable by this name, build one and register it with the
        model. Otherwise, just update the existing node. The contents of {value} can refer to
        other variables in the model by following the rules in pyre.calc.Expression, and may
        make certain calls to the python runtime. The exact details are being worked out...
        """
        # check whether we have seen this variable before
        try:
            node = self.findNode(name)
        except KeyError:
            # if not, build one and register it
            node = Variable(value=None, evaluator=None)
            self.registerNode(name=name, node=node)
        else:
            # bail out if we have seen this node before and we are not performing replacement
            # binding
            if not replace: return

        # build an evaluator
        # figure out if this value contains references to other nodes
        if value and Expression._scanner.match(value):
            evaluator = Expression(expression=value, model=self)
            value = None
        else:
            evaluator = None

        # figure where to attach the evaluator
        if evaluator:
            node.evaluator = evaluator
        else:
            node.value = value

        # log the event
        self._tracker.track(key=node, value=(value, locator))

        # return the node
        return node


    # interface obligations from the abstract base class
    def addNode(self, name, node):
        """
        Implementation details of the mechanism for node insertion in the model: associate
        {node} with {name} and insert into the model

        If you are looking to insert a node in the model, please use 'registerNode',
        which is a lot smarter and takes care of patching unresolved names.
        """
        # hash the name
        key = self._hash.hash(name, separator=self.SEPARATOR)
        # add the node the node store
        self._nodes[key] = node
        # add the name to the name store
        self._names[key] = name
        # all done
        return


    def findNode(self, name):
        """
        Locate the node in the model that matches {name}.
        """
        return self._nodes[self._hash.hash(name, separator=self.SEPARATOR)]
        

    def getNodes(self):
        """
        Iterate over the nodes in my graph.

        This is expected to return a sequence of ({name}, {node}) tuples, regardless of the
        node storage details implemented by AbstractModel descendants
        """
        # for each of my registered nodes
        for key, node in self._nodes.items():
            # look up the associated name and yield the required value
            yield self._names[key], node
        # all done
        return


    # meta methods
    def __init__(self, name=None, **kwds):
        name = name if name is not None else "pyre.evaluator"
        super().__init__(name=name, **kwds)

        # model evaluation support
        self._names = {}
        self._nodes = {}
        self._hash = pyre.patterns.newPathhash()

        # history tracking
        self._tracker = pyre.tracking.newTracker()

        return


# end of file 
