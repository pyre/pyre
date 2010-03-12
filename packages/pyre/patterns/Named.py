# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


class Named(object):
    """
    Base class for objects that have names
    """


    def __init__(self, *, name, **kwds):
        super().__init__(**kwds)
        self.name = name
        return


# end of file 
