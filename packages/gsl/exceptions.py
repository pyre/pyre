# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


class GSLError(Exception):
    """
    Base class for all GSL related errors
    """

    def __init__(self, description, **kwds):
        super().__init__(**kwds)
        self.description = description
        return

    def __str__(self):
        # return the error description
        return self.description


# end of file 
