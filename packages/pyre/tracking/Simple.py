# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


class Simple:
    """
    A locator that records a simple named source with no further details
    """


    # meta methods
    def __init__(self, source):
        self.source = source
        return


    def __str__(self):
        return str(self.source)


    # implementation details
    __slots__ = "source",


# end of file
