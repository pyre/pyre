# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


class Unresolved:
    """
    A node that raises {UnresolvedNodeError} when its value is read
    """


    # exceptions
    from .exceptions import UnresolvedNodeError


    # public data
    name = None # the unresolved name


    @property
    def getValue(self):
        """
        Compute my value
        """
        raise self.UnresolvedNodeError(node=self, name=self.request)


    # meta methods
    def __init__(self, request, **kwds):
        super().__init__(**kwds)
        self.request = request
        return


    # private data
    _value = None # the cache is permanently dirty


# end of file 
