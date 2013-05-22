# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
from .. import schemata
# superclass
from .Sequence import Sequence


# declaration
class List(Sequence):
    """
    A property that represents lists
    """


    # public data
    default = []


    # interface
    def coerce(self, value, **kwds):
        """
        Walk {value} through the casting procedure
        """
        # leave {None} alone
        if value is None: return None
        # easy enough for me
        return list(super().coerce(value, **kwds))


    # meta-methods
    def __init__(self, default=default, **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file 
