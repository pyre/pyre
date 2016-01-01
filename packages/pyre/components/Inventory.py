# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# superclass
from ..framework.Dashboard import Dashboard


# declaration
class Inventory(dict, Dashboard):
    """
    Base class for the state storage strategies for component classes and instances
    """


    # public data
    name = None # by default, components have no name
    package = None # by default, components have no family names


    # interface
    @classmethod
    def initializeClass(cls):
        """
        Build inventory for a component class
        """
        # implementation dependent -- override in subclasses
        raise NotImplementedError(
            "class {.__name__!r} must implement 'initializeClass'".format(cls))


    @classmethod
    def initializeInstance(cls):
        """
        Build inventory for a component instance
        """
        # implementation dependent -- override in subclasses
        raise NotImplementedError(
            "class {.__name__!r} must implement 'inistializeInstance'".format(cls))


    # meta-methods
    def __init__(self, slots, **kwds):
        super().__init__(**kwds)
        # load the slots
        self.update(slots)
        # all done
        return


# end of file
