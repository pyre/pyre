# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# superclass
from .Executive import Executive


# declaration
class Inventory(dict, Executive):
    """
    Base class for the state storage strategies for component classes and instances
    """


    # interface
    @classmethod
    def classInventory(cls):
        """
        """
        raise NotImplementedError(
            "class {.__name__!r} must implement 'classInventory'".format(cls))


    @classmethod
    def instanceInventory(cls):
        """
        """
        raise NotImplementedError(
            "class {.__name__!r} must implement 'instanceInventory'".format(cls))


    # meta-methods
    def __init__(self, slots, **kwds):
        super().__init__(**kwds)
        # load the slots
        self.update(slots)
        # all done
        return


# end of file 
