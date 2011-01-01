# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


class Simple:
    """
    Locator that records a simple named source with no further details
    """


    # public data
    source = None


    # meta methods
    def __init__(self, source, **kwds):
        super().__init__(**kwds)
        self.source = source
        return


    def __str__(self):
        return self.source


# end of file 
