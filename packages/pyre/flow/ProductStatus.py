# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# my superclasses
from .Status import Status


# declaration
class ProductStatus(Status):
    """
    A helper that watches over the traits of products and records value changes
    """

    # interface
    def addInputBinding(self, factory, product):
        """
        My client {product} is an input to {factory}
        """
        # add the {factory} monitor to my observers
        return self.addObserver(observer=factory.pyre_status)


    def removeInputBinding(self, factory, product):
        """
        My client {product} is no longer an input to {factory}
        """
        # remove the {factory} monitor from my pile of observers
        return self.removeObserver(observer=factory.pyre_status)


    def addOutputBinding(self, factory, product):
        """
        Add my client {product} as an output of {factory}
        """
        # my client is associated with a new factory, so mark me as stale and notify downstream
        return self.flush(observable=factory.pyre_status)


# end of file
