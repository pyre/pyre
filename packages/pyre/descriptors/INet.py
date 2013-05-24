# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
from .. import schemata
# superclass
from . import descriptor


# declaration
class INet(descriptor):
    """
    A property that represents internet addresses
    """


    # public data
    default = schemata.inet.any
    schema = schemata.inet


    # meta-methods
    def __init__(self, default=default, **kwds):
        # chain up
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file 
