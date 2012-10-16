# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


class Named:
    """
    Base class for objects that have names
    """

    
    # public data
    name = None


    # meta-methods
    def __init__(self, *, name=None, **kwds):
        super().__init__(**kwds)
        self.name = name
        return


# end of file 
