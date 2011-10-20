# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# the metaclass
from .Selector import Selector


# declaration
class Query(metaclass=Selector):
    """
    Base class for describing database queries
    """


# end of file 
