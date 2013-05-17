# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# urban radish
# (c) 2011-2013 all rights reserved
#


# access to the framework
import pyre
# and my protocols
from .DataStore import DataStore


# declaration
class Client(pyre.component, family="pyre.db.client"):
    """
    The base class for components that connect to data stores
    """

    # user configurable state
    db = DataStore()


# end of file 
