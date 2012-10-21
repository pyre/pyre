# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


class NameLookup:
    """
    A locator that records a simple named source with no further details
    """


    # meta methods
    def __init__(self, description, key):
        self.key = key
        self.description = description
        return


    def __str__(self):
        # get access to the framework managers
        from ..components.Executive import Executive
        # generate my rep
        return "{} {}".format(self.description, Executive.pyre_nameserver[self.key])


    # implementation details
    __slots__ = "key", "description"


# end of file
