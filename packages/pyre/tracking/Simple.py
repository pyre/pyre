# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


class Simple(object):
    """
    Locator that records a simple named source with no further details
    """


    # public date
    source = None


    # meta methods
    def __init__(self, source, **kwds):
        super().__init__(**kwds)
        self.source = source
        return


    def __str__(self):
        return self.source


# end of file 
