# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import weakref
import collections
from pyre.calc.HierarchicalModel import HierarchicalModel


class Model(HierarchicalModel):
    """
    A specialization of a hierarchical model that takes into account that the model nodes have
    priorities attached to them and cannot indiscriminately replace each other
    """


    # types
    from .Slot import Slot


    # public data
    defaultPriority = None # the default priority to assign to ne slots


    # interface
    def recognize(self, value, priority=None):
        """
        Attempt to decipher {value} and build a slot to hold it
        """
        # get my ancestor to build the slot
        slot = super().recognize(value)
        # adjust its priority
        slot._priority = priority if priority is not None else self.defaultPriority
        # and return it to the caller
        return slot


    # configuration event processing
    def bind(self, key, value, priority=None, locator=None):
        """
        Build a node with the given {priority} to hold {value}, and register it under {key}
        """
        # build a new node 
        slot = self.recognize(value=value, priority=priority)
        # get it registered
        return self.register(node=slot, key=key)


    def defer(self, component, family, key, value, locator, priority):
        """
        Build a node that corresponds to a conditional configuration
        """
        # print("Model.defer:")
        # print("    component={}, family={}".format(component, family))
        # print("    key={}, value={!r}".format(key, value))
        # print("    from {}".format(locator))
        # print("    with priority {}".format(priority))

        # hash the component name
        ckey = self._hash.hash(component)
        # hash the family key
        fkey = self._hash.hash(family)
        # get the deferred event store
        model = self.deferred[(ckey, fkey)]
        # build a slot
        slot = self.recognize(value=value, priority=priority)
        # and add it to the pile
        model.append( (key, slot) )
        # all done
        return slot


    def load(self, source, locator, **kwds):
        """
        Ask the pyre {executive} to load the configuration settings in {source}
        """
        # get the executive to kick start the configuration loading
        self.executive.loadConfiguration(uri=source, locator=locator)
        # and return
        return self


    # factory for my nodes
    def newNode(self, evaluator):
        """
        Create a new node with the given evaluator
        """
        # why is this the right node factory?
        # subclasses should override this to provide their own nodes to host the evaluator
        return self.Slot(value=None, evaluator=evaluator, priority=self.defaultPriority)


    # meta methods
    def __init__(self, executive, defaultPriority, **kwds):
        super().__init__(**kwds)
        # record the executive
        self.executive = weakref.proxy(executive)
        # the default priority for new slots
        self.defaultPriority = defaultPriority
        # the database of deferred bidings
        self.deferred = collections.defaultdict(list)
        return


# end of file 
