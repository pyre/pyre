# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


class Info:
    """
    Base class for encapsulating nodal metadata for filesystem entries
    """


    # meta methods
    def __init__(self, uri, **kwds):
        super().__init__(**kwds)
        self.uri = uri
        return


    # implementation details
    __slots__ = ('uri')


# end of file 
