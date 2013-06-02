# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
from .. import schemata
# superclass
from .Slotted import Slotted


@schemata.typed
class Property(Slotted):
    """
    The base class for attribute descriptors that describe a component's external state
    """


    # meta-methods
    def __str__(self):
        return "{0.name}: a property of type {0.schema}".format(self)


# end of file 
