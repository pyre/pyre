# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


class Chain:
    """
    A locator that ties together two others in order to express that something in {next}
    caused {this} to be recorded
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
