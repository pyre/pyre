# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# externals
import pyre
# my base class
from .Node import Node


# declaration
class Server(Node):
    """
    Base class for components that are aware of the network
    """


    # public state
    address = pyre.properties.inet()


    # meta methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)

        # all done
        return


# end of file 
