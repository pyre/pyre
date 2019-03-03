# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# support
import pyre
# my protocol
from .Specification import Specification
# my superclass
from .Node import Node
# my status tracker
from .Status import Status


# class declaration
class Product(Node, implements=Specification):
    """
    The base class for data products
    """


    # public data
    # the object that watches over my traits
    status = None


    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # build my status tracker
        self.status = Status().track(component=self)
        # all done
        return


# end of file
