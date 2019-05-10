# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# my superclasses
from .Status import Status
from .Stale import Stale


# declaration
class ProductStatus(Stale, Status):
    """
    A helper that watches over the traits of products and records value changes
    """

    # N.B. the {flush} chain terminates in the {Status} branch of the inheritance so it has to
    # be last in the sequence of ancestors

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


    # meta-methods
    def __init__(self, stale=False, **kwds):
        # chain up
        super().__init__(stale=stale, **kwds)
        # all done
        return


# end of file
