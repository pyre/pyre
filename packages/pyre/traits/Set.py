# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
from .. import schemata
# superclass
from .Property import Property


# declaration
class Set(Property):
    """
    A property that represents sets
    """


    # public data
    default = set()


    # interface
    def coerce(self, value, **kwds):
        """
        Walk {value} through the casting procedure
        """
        # leave {None} alone
        if value is None: return None
        # easy enough for me
        return set(super().coerce(value, **kwds))


    # meta-methods
    def __init__(self, default=default, **kwds):
        # chain up with my default
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file 
