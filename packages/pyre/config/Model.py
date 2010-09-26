# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from pyre.calc.HierarchicalModel import HierarchicalModel


class Model(HierarchicalModel):
    """
    A specialization of a hierarchical model that takes into account that the model nodes have
    priorities attached to them and cannot indiscriminately replace each other
    """


    # types
    from .Slot import Slot


    # interface
    def bind(self, key, value, priority):
        """
        Build a node with the given {priority} to hold {value}, and register it under {key}
        """
        # build a new node 
        slot = self.recognize(value)
        # adjust its priority
        slot._priority = priority
        # get it registered
        # N.B.: the call to tuple forces the realization of generators; it is necessary because
        # register may need to iterate over the key multiple times
        self.register(node=slot, key=tuple(key))
        # and return the new slot to the caller
        return slot


    # overriden methods
    def patch(self, *, old, new):
        """
        Patch the evaluation graph by grafting {new} in the place of {old}

        This method performs collision resolution for slots that are nominally indistinguishable.
        """
        # old and new are both guaranteed to be slot instances
        # if {new} overrides {old}
        if new._priority >= old._priority:
            # MGA
            print("pyre.config.Model.patch: NYI: transfer slot information")
            super().patch(old=old, new=new)
        # otherwise, return the old node
        return old


    # factory for my nodes
    def newNode(self, evaluator):
        """
        Create a new node with the given evaluator
        """
        # why is this the right node factory?
        # subclasses should override this to provide their own nodes to host the evaluator
        return self.Slot(value=None, evaluator=evaluator, priority=self.defaultPriority)


    # meta methods
    def __init__(self, defaultPriority, **kwds):
        super().__init__(**kwds)
        self.defaultPriority = defaultPriority
        return


# end of file 
