# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


# superclass
from ..framework.Dashboard import Dashboard


# declaration
class Inventory(Dashboard):
    """
    Base class for the state storage strategies for component classes and instances
    """


    # public data
    name = None # by default, components have no name
    fragments = () # by default, components have no family name
    package = None # by default, components don't belong to a package


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
        # chain up
        super().__init__(**kwds)
        # initialize my table
        self.traits = {}
        # load the slots
        self.traits.update(slots)
        # all done
        return


    def __getitem__(self, trait):
        # ask my table
        return self.traits[trait]


    def __setitem__(self, trait, item):
        # punt
        self.traits[trait] = item
        # all done
        return


# end of file
