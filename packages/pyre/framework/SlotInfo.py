# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# superclass
from ..calc.NodeInfo import NodeInfo


# declaration
class SlotInfo(NodeInfo):
    """
    Encapsulation of the slot metadata maintained by the nameserver
    """


    # types
    from .Priority import Priority as priorities
    from ..traits.Property  import Property as properties


    # public data
    locator = None # provenance
    priority = None # the rank of this setting
    trait = None # the type information


    # meta-methods
    def __init__(self, priority=None, locator=None, trait=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my metadata
        self.locator = locator
        self.priority = priority or self.priorities.uninitialized()
        self.trait = trait or self.properties.identity().instanceSlot
        # all done
        return


# end of file 
