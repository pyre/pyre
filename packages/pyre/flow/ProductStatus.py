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

    # meta-methods
    def __init__(self, stale=False, **kwds):
        # chain up
        super().__init__(stale=stale, **kwds)
        # all done
        return


    # hooks
    def monitorFactory(self, factory):
        """
        Add {factory} to my pile of observables
        """
        # get the factory status monitor
        monitor = factory.pyre_status
        # let it know
        return monitor.addObserver(observer=self)


# end of file
