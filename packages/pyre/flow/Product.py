# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# externals
import weakref
# support
import pyre
# my protocol
from .Specification import Specification
# my superclass
from .Node import Node


# class declaration
class Product(Node, implements=Specification, internal=True):
    """
    The base class for data products
    """


    # public data
    @property
    def pyre_stale(self):
        """
        Retrieve my status
        """
        # delegate to my status manager
        return self.pyre_status.stale

    @pyre_stale.setter
    def pyre_stale(self, value):
        """
        Set my status
        """
        # delegate to my status manager
        self.pyre_status.stale = value
        # all done
        return


    # interface
    def sync(self):
        """
        Examine my state
        """


    @pyre.export
    def pyre_make(self):
        """
        Invoke my factories to update me
        """
        # if i am not stale
        if not self.pyre_stale:
            # nothing to do
            return self
        # otherwise, go through my factories
        for factory in self.pyre_factories:
            # and ask each one to update me
            factory.pyre_make(product=self)
        # if all went well, update my status
        self.pyre_stale = False
        # all done
        return self


        # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # initialize the list of my factories
        self.pyre_factories = weakref.WeakSet()
        # all done
        return


    # flow hooks
    def pyre_newStatus(self, **kwds):
        """
        Build a handler for my status changes
        """
        # grab the factory
        from .ProductStatus import ProductStatus
        # make one and return it
        return ProductStatus(**kwds)


    def pyre_registerFactory(self, factory):
        """
        Register {factory} as one of my makers
        """
        # add the {factory} to my pile
        self.pyre_factories.add(factory)
        # set it up so i can monitor its status
        self.pyre_status.monitorFactory(factory=factory)
        # all done
        return self



# end of file
