# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# superclass
from ..framework.Client import Client


# declaration
class Inventory(dict, Client):
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


    # implementation details
    def hashKey(cls, **kwds):
        """
        Build a hash key for a trait slot that is about to be minted
        """
        # implementation dependent -- override in subclasses
        raise NotImplementedError(
            "class {.__name__!r} must implement 'hashKey'".format(cls))


    # meta-methods
    def __init__(self, slots, **kwds):
        super().__init__(**kwds)
        # load the slots
        self.update(slots)
        # all done
        return


# end of file 
