# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


class Chain:
    """
    Locator that ties two others together
    """


    # public data
    this = None
    next = None


    # meta methods
    def __init__(self, this, next, **kwds):
        super().__init__(**kwds)
        self.this = this
        self.next = next
        return


    def __str__(self):
        return "{0.this} via {0.next}".format(self)


# end of file 
